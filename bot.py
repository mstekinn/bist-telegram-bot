import telebot
import yfinance as yf
from google import genai
import os # Çevre değişkenleri için eklendi

# --- 1. AYARLAR VE GİRİŞ BİLGİLERİ ---

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


# --- 2. FONKSİYONLAR ---

@bot.message_handler(commands=['bulten'])
def bulten_gonder(message):
    CHAT_ID = message.chat.id
    
    try:
        bot.reply_to(message, "⏳ Bültenter taranıyor ve yapay zeka analizi hazırlanıyor... Bu işlem birkaç dakika sürebilir, lütfen bekleyin.")
        
        bist100_hisseleri = [
            'AEFES.IS', 'AGHOL.IS', 'AHGAZ.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKFGY.IS', 'AKFYE.IS', 'AKSA.IS', 'AKSEN.IS', 'ALARK.IS',
            'ALBRK.IS', 'ALFAS.IS', 'ANSGR.IS', 'ARCLK.IS', 'ASELS.IS', 'ASTOR.IS', 'BERA.IS', 'BIENY.IS', 'BIMAS.IS', 'BOBET.IS',
            'BRSAN.IS', 'BRYAT.IS', 'BUCIM.IS', 'CANTE.IS', 'CCOLA.IS', 'CIMSA.IS', 'CWENE.IS', 'DOAS.IS', 'DOHOL.IS', 'EBEBK.IS',
            'ECILC.IS', 'ECZYT.IS', 'EGEEN.IS', 'EKGYO.IS', 'ENKAI.IS', 'ENJSA.IS', 'EREGL.IS', 'EUPWR.IS', 'FROTO.IS', 'GARAN.IS',
            'GESAN.IS', 'GUBRF.IS', 'GWIND.IS', 'HALKB.IS', 'HEKTS.IS', 'IMASM.IS', 'INVES.IS', 'ISCTR.IS', 'ISGYO.IS', 'ISMEN.IS',
            'KAYSE.IS', 'KCAER.IS', 'KCHOL.IS', 'KLSER.IS', 'KONTR.IS', 'KORDS.IS', 'KOZAL.IS', 'KOZAA.IS', 'KRDMD.IS', 'KTLEV.IS',
            'LMKDC.IS', 'MAALT.IS', 'MAVI.IS', 'MHRGY.IS', 'MIATK.IS', 'MTRKS.IS', 'OTKAR.IS', 'OYYAT.IS', 'PETKM.IS', 'PGSUS.IS',
            'QUAGR.IS', 'REEDR.IS', 'SAHOL.IS', 'SASA.IS', 'SDTTR.IS', 'SISE.IS', 'SKBNK.IS', 'SMRTG.IS', 'SOKM.IS', 'TABGD.IS',
            'TAVHL.IS', 'TCELL.IS', 'THYAO.IS', 'TKFEN.IS', 'TOASO.IS', 'TSKB.IS', 'TTKOM.IS', 'TTRAK.IS', 'TUPRS.IS', 'TURSG.IS',
            'ULKER.IS', 'VAKBN.IS', 'VESBE.IS', 'VESTL.IS', 'YEOTK.IS', 'YKBNK.IS', 'YYLGD.IS', 'ZOREN.IS'
        ]
        
        fiyat_ve_haber_bilgileri = ""
        
        # Tüm BIST 100 hisselerinin fiyat trendini ve haberlerini çek
        for hisse in bist100_hisseleri:
            try:
                ticker = yf.Ticker(hisse)
                
                # 1. Adım: Son 5 günlük veriyi çek
                veri = ticker.history(period="5d")
                
                if not veri.empty:
                    kapanislar = veri['Close'].tolist()
                    hisse_adi = hisse.replace('.IS', '')
                    fiyatlar_str = " - ".join([f"{f:.2f}" for f in kapanislar])
                    
                    # 2. Adım: Hisseyle ilgili haberleri çek
                    haberler = ticker.news
                    haber_metni = ""
                    
                    if haberler and len(haberler) > 0:
                        haber_basliklari = [haber.get('title', '') for haber in haberler[:2] if haber.get('title')]
                        if haber_basliklari:
                            haber_metni = " | ".join(haber_basliklari)
                        else:
                            haber_metni = "Güncel haber yok."
                    else:
                        haber_metni = "Güncel haber yok."
                        
                    # 3. Adım: Fiyat ve haberleri tek bir satırda birleştir
                    fiyat_ve_haber_bilgileri += f"{hisse_adi} | Trend: {fiyatlar_str} | Haberler: {haber_metni}\n"
            except:
                continue 
        
        if fiyat_ve_haber_bilgileri != "":
            # Gemini'ye kapsamlı talimatı veriyoruz
            ozet_bilgi = (
                "Sen uzman bir borsa analistisin. Aşağıda BIST 100 endeksindeki hisselerin son 5 günlük kapanış fiyat trendleri "
                "ve varsa en güncel haber başlıkları listelenmiştir:\n\n"
                f"{fiyat_ve_haber_bilgileri}\n"
                "GÖREVİN:\n"
                "1. Fiyat hareketlerini teknik olarak incele.\n"
                "2. Haber başlıklarındaki olumlu veya olumsuz gelişmeleri (temel analiz) değerlendir ve fiyat trendiyle birleştir.\n"
                "3. Her iki kritere göre yükseliş potansiyeli en yüksek 5 hisseyi (KARAR: AL) ve düşüş potansiyeli en yüksek 5 hisseyi (KARAR: SAT) belirle.\n"
                "4. Sadece seçtiğin bu 10 hisse için KESİNLİKLE aşağıdaki formatı kullanarak alt alta listeleme yap. Başka hiçbir kelime veya yorum YAZMA:\n\n"
                "Hisse: [HİSSE KODU]\n"
                "KARAR: [AL veya SAT]\n"
                "Destek 1: [Fiyat] TL\n"
                "Destek 2: [Fiyat] TL\n"
                "Direnç 1: [Fiyat] TL\n"
                "Direnç 2: [Fiyat] TL\n"
                "----------------------"
            )
            
            response = client.models.generate_content(
                model='gemini-3-flash-preview', 
                contents=ozet_bilgi
            )
            
            analiz_metni = response.text
            
            bot.send_message(CHAT_ID, f"📊 **Teknik & Haber Destekli Hisse Analizi (Günün 10 Hissesi):**\n\n{analiz_metni}", parse_mode="Markdown")
            
        else:
            bot.send_message(CHAT_ID, "Bülten için veri çekilemedi.")
            
    except Exception as e:
        hata_mesaji = f"Bülten hazırlanırken bir hata oluştu: {e}"
        bot.send_message(CHAT_ID, hata_mesaji)

@bot.message_handler(commands=['analiz'])
def tek_hisse_analiz_et(message):
    try:
        komut_bolumleri = message.text.split()
        
        if len(komut_bolumleri) < 2:
            bot.reply_to(message, "Lütfen bir hisse kodu girin. Örnek: /analiz KCHOL")
            return
            
        hisse_kodu = komut_bolumleri[1].upper()
        if not hisse_kodu.endswith(".IS"):
            hisse_kodu += ".IS"
            
        bot.reply_to(message, f"{hisse_kodu} için veriler çekiliyor, lütfen bekleyin...")
        
        hisse = yf.Ticker(hisse_kodu)
        veri = hisse.history(period="1mo")
        
        if veri.empty:
            bot.reply_to(message, "Veri bulunamadı. Lütfen geçerli bir borsa kodu yazdığınızdan emin olun.")
            return
            
        son_kapanis = veri['Close'].iloc[-1]
        
        prompt = (
            f"Hisse: {hisse_kodu}\n"
            f"Son Kapanış: {son_kapanis:.2f} TL\n"
            "Sen bir borsa uzmanısın. Lütfen bu hisse için KESİNLİKLE sadece aşağıdaki formatta, başka hiçbir açıklama veya yorum eklemeden cevap ver:\n\n"
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
        
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, f"Analiz sırasında bir hata oluştu: {e}")


# --- 3. BOTU ÇALIŞTIRMA ---

print("Borsa Yapay Zeka Botu başarıyla başlatıldı ve dinleniyor...")
print("Komutlar aktif: Telegram üzerinden /bulten veya /analiz [HİSSE] yazarak kullanabilirsiniz.")

bot.infinity_polling()