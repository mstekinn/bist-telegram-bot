import telebot
import yfinance as yf
from google import genai
import os
import pandas_ta as ta
import concurrent.futures # Hızlandırma (Threading) için EKLENDİ

# --- 1. AYARLAR VE GİRİŞ BİLGİLERİ ---

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Çevresel değişkenden ID'yi al ve tam sayıya (integer) çevir
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

# GÜVENLİK: Sadece bu ID'lere sahip kişiler botu kullanabilir
YETKILI_KULLANICILAR = [ADMIN_ID]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


# --- HIZLANDIRMA İÇİN YARDIMCI FONKSİYON ---
def tek_hisse_verisi_cek(hisse):
    """Bülten taramasını hızlandırmak için her hisseyi ayrı iş parçacığında çeken fonksiyon."""
    try:
        ticker = yf.Ticker(hisse)
        veri = ticker.history(period="5d")
        
        if veri.empty:
            return ""
            
        kapanislar = veri['Close'].tolist()
        hisse_adi = hisse.replace('.IS', '')
        fiyatlar_str = " - ".join([f"{f:.2f}" for f in kapanislar])
        
        haberler = ticker.news
        if haberler and len(haberler) > 0:
            haber_basliklari = [haber.get('title', '') for haber in haberler[:2] if haber.get('title')]
            haber_metni = " | ".join(haber_basliklari) if haber_basliklari else "Güncel haber yok."
        else:
            haber_metni = "Güncel haber yok."
            
        return f"{hisse_adi} | Trend: {fiyatlar_str} | Haberler: {haber_metni}\n"
    except:
        return ""


# --- 2. ANA FONKSİYONLAR ---

@bot.message_handler(commands=['bulten'])
def bulten_gonder(message):
    CHAT_ID = message.chat.id
    
    # YETKİ KONTROLÜ
    if CHAT_ID not in YETKILI_KULLANICILAR:
        bot.send_message(CHAT_ID, "⛔ Bu botu kullanma yetkiniz bulunmamaktadır.")
        return
    
    try:
        bot.reply_to(message, "⏳ BIST 100 Bülteni taranıyor... 100 hissenin teknik verileri ve haberleri inceleniyor, bu işlem 1-2 dakika sürebilir, lütfen bekleyin!")
        
        # BIST 100 HİSSELERİ (Güncel ve hacimli hisseler)
        bist100_hisseleri = [
            'AEFES.IS', 'AGHOL.IS', 'AHGAZ.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKFYE.IS', 'AKSA.IS', 'AKSEN.IS', 'ALARK.IS', 'ALBRK.IS', 
            'ALFAS.IS', 'ARCLK.IS', 'ASELS.IS', 'ASTOR.IS', 'ASUZU.IS', 'AYDEM.IS', 'BAGFS.IS', 'BERA.IS', 'BIENY.IS', 'BIMAS.IS', 
            'BIOEN.IS', 'BOBET.IS', 'BRSAN.IS', 'BRYAT.IS', 'BUCIM.IS', 'CANTE.IS', 'CCOLA.IS', 'CIMSA.IS', 'CWENE.IS', 'DOAS.IS', 
            'DOHOL.IS', 'ECILC.IS', 'ECZYT.IS', 'EGEEN.IS', 'EKGYO.IS', 'ENJSA.IS', 'ENKAI.IS', 'EREGL.IS', 'EUPWR.IS', 'EUREN.IS', 
            'FROTO.IS', 'GARAN.IS', 'GENIL.IS', 'GESAN.IS', 'GLYHO.IS', 'GUBRF.IS', 'GWIND.IS', 'HALKB.IS', 'HEKTS.IS', 'HLGYO.IS', 
            'IMASM.IS', 'INVEO.IS', 'INVES.IS', 'IPEKE.IS', 'ISCTR.IS', 'ISDMR.IS', 'ISFIN.IS', 'ISGYO.IS', 'ISMEN.IS', 'IZENR.IS', 
            'KALES.IS', 'KARSN.IS', 'KAYSE.IS', 'KCAER.IS', 'KCHOL.IS', 'KMPUR.IS', 'KONTR.IS', 'KONYA.IS', 'KOZAA.IS', 'KOZAL.IS', 
            'KRDMD.IS', 'KZBGY.IS', 'MAVI.IS', 'MGROS.IS', 'MIATK.IS', 'ODAS.IS', 'OTKAR.IS', 'OYAKC.IS', 'PENTI.IS', 'PETKM.IS', 
            'PGSUS.IS', 'PNLSN.IS', 'QUAGR.IS', 'SAHOL.IS', 'SASA.IS', 'SAYAS.IS', 'SISE.IS', 'SKBNK.IS', 'SMRTG.IS', 'SOKM.IS', 
            'TAVHL.IS', 'TCELL.IS', 'THYAO.IS', 'TKFEN.IS', 'TOASO.IS', 'TSKB.IS', 'TTKOM.IS', 'TTRAK.IS', 'TUPRS.IS', 'VAKBN.IS', 
            'VESBE.IS', 'VESTL.IS', 'YEOTK.IS', 'YKBNK.IS', 'YYLGD.IS', 'ZOREN.IS'
        ]
        
        fiyat_ve_haber_bilgileri = ""
        
        # HIZLANDIRMA: max_workers 20 yapılarak 100 hissenin verisi çok daha hızlı çekiliyor
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            sonuclar = list(executor.map(tek_hisse_verisi_cek, bist100_hisseleri))
            
        for sonuc in sonuclar:
            fiyat_ve_haber_bilgileri += sonuc
        
        if fiyat_ve_haber_bilgileri != "":
            ozet_bilgi = (
                "Sen uzman bir borsa analistisin. Aşağıda BIST 100 endeksindeki hisselerin son 5 günlük kapanış fiyat trendleri "
                "ve varsa en güncel haber başlıkları listelenmiştir:\n\n"
                f"{fiyat_ve_haber_bilgileri}\n"
                "GÖREVİN:\n"
                "1. Fiyat hareketlerini teknik olarak incele.\n"
                "2. Haber başlıklarındaki olumlu veya olumsuz gelişmeleri değerlendir.\n"
                "3. Tüm bu hisseler arasından yükseliş potansiyeli EN YÜKSEK 10 hisseyi (KARAR: AL) belirle.\n"
                "4. Sadece seçtiğin bu 10 hisse için KESİNLİKLE aşağıdaki formatı kullanarak alt alta listeleme yap. Başka hiçbir açıklama, yorum veya kelime YAZMA:\n\n"
                "Hisse: [HİSSE KODU]\n"
                "Güncel Fiyat: [Gönderdiğim son günün fiyatı] TL\n"
                "KARAR: AL\n"
                "Destek 1: [Fiyat] TL\n"
                "Direnç 1: [Fiyat] TL\n"
                "----------------------"
            )
            
            response = client.models.generate_content(
                model='gemini-3-flash-preview', 
                contents=ozet_bilgi
            )
            
            yasal_uyari = "\n\n⚠️ *Yasal Uyarı:* Veriler Yahoo Finance üzerinden sağlanmaktadır ve BIST kuralları gereği 15 dk gecikmeli olabilir. Analizler yapay zeka desteklidir, kesinlikle yatırım tavsiyesi (YTD) değildir."
            
            bot.send_message(CHAT_ID, f"📊 **BIST 100 Yapay Zeka Günlük Önerileri (Top 10):**\n\n{response.text}{yasal_uyari}", parse_mode="Markdown")
            
        else:
            bot.send_message(CHAT_ID, "Bülten için veri çekilemedi. Lütfen daha sonra tekrar deneyin.")
            
    except Exception as e:
        bot.send_message(CHAT_ID, f"Bülten hazırlanırken bir hata oluştu: {e}")


@bot.message_handler(commands=['analiz'])
def tek_hisse_analiz_et(message):
    CHAT_ID = message.chat.id
    
    # YETKİ KONTROLÜ
    if CHAT_ID not in YETKILI_KULLANICILAR:
        bot.send_message(CHAT_ID, "⛔ Bu botu kullanma yetkiniz bulunmamaktadır.")
        return
        
    try:
        komut_bolumleri = message.text.split()
        
        if len(komut_bolumleri) < 2:
            bot.reply_to(message, "Lütfen bir hisse kodu girin. Örnek: /analiz KCHOL")
            return
            
        hisse_kodu = komut_bolumleri[1].upper()
        if not hisse_kodu.endswith(".IS"):
            hisse_kodu += ".IS"
            
        bot.reply_to(message, f"{hisse_kodu} için teknik veriler ve indikatörler hesaplanıyor, lütfen bekleyin...")
        
        hisse = yf.Ticker(hisse_kodu)
        veri = hisse.history(period="3mo")
        
        if veri.empty:
            bot.reply_to(message, "Veri bulunamadı. Lütfen geçerli bir borsa kodu yazdığınızdan emin olun.")
            return
            
        veri.ta.rsi(length=14, append=True)
        veri.ta.sma(length=20, append=True)
        
        # HATA ÖNLEYİCİ GÜVENLİK KONTROLÜ (YENİ EKLENEN KISIM)
        if 'RSI_14' not in veri.columns or 'SMA_20' not in veri.columns:
            bot.reply_to(message, "⚠️ Bu hisse için yeterli geçmiş veri bulunamadı. (Hisse yeni halka arz olmuş veya yeterli işlem gününe ulaşmamış olabilir).")
            return
            
        son_kapanis = veri['Close'].iloc[-1]
        son_rsi = veri['RSI_14'].iloc[-1]
        son_sma = veri['SMA_20'].iloc[-1]
        
        prompt = (
            f"Hisse: {hisse_kodu}\n"
            f"Son Kapanış: {son_kapanis:.2f} TL\n"
            f"14 Günlük RSI: {son_rsi:.2f}\n"
            f"20 Günlük Hareketli Ortalama (SMA): {son_sma:.2f} TL\n\n"
            "Sen uzman bir borsa analistisin. Yukarıdaki matematiksel teknik indikatörleri "
            "(RSI aşırı alım/satım bölgelerini ve fiyatın ortalamaya göre konumunu) dikkate alarak "
            "bu hisse için KESİNLİKLE sadece aşağıdaki formatta, başka hiçbir açıklama veya yorum eklemeden cevap ver:\n\n"
            "Güncel Fiyat: {son_kapanis:.2f} TL\n"
            "KARAR: [AL / SAT veya TUT]\n\n"
            "Destek 1: [Fiyat] TL\n"
            "Destek 2: [Fiyat] TL\n"
            "Direnç 1: [Fiyat] TL\n"
            "Direnç 2: [Fiyat] TL"
        )
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview', 
            contents=prompt
        )
        
        # YASAL UYARI EKLENTİSİ
        yasal_uyari = "\n\n⚠️ *Yasal Uyarı:* Veriler 15 dk gecikmeli olabilir. Bu analiz yatırım tavsiyesi (YTD) değildir."
        
        bot.reply_to(message, f"{response.text}{yasal_uyari}")
        
    except Exception as e:
        bot.reply_to(message, f"Analiz sırasında bir hata oluştu: {e}")


# --- 3. BOTU ÇALIŞTIRMA ---

print("Borsa Yapay Zeka Botu başarıyla başlatıldı ve dinleniyor...")
print("Komutlar aktif: Telegram üzerinden /bulten veya /analiz [HİSSE] yazarak kullanabilirsiniz.")

bot.infinity_polling()
