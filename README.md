📈 AI-Powered Stock Analysis Telegram Bot (BIST 30)
Bu proje, Borsa İstanbul (BIST) hisselerini anlık olarak tarayan, teknik indikatörler ile matematiksel analiz yapan ve Google Gemini AI kullanarak duygu/trend analizi gerçekleştiren otonom bir Telegram botudur.

Geleneksel finansal veri çekme yöntemlerini, modern yapay zeka yorumlama yetenekleriyle birleştirerek kullanıcılara hızlı ve yapılandırılmış destek/direnç raporları sunar.

🚀 Özellikler
Çoklu İşlem (Multi-Threading) ile Yüksek Performans: 100'e yakın hissenin verisi sırayla değil, concurrent.futures kullanılarak asenkron olarak çekilir. Bülten tarama süresi dakikalardan saniyelere indirilmiştir.

Matematiksel Tutarlılık: AI modelinin halüsinasyon görmesini engellemek için pandas-ta kütüphanesi kullanılarak 14 Günlük RSI ve 20 Günlük SMA (Hareketli Ortalama) gibi teknik veriler hesaplanarak modele beslenir.

Beyaz Liste (Whitelist) Güvenliği: Sistemin kötüye kullanımını ve API kotalarının aşılmasını engellemek için özel bir Telegram ID yetkilendirme algoritması kullanılmıştır. Sadece yetkili kullanıcılar botla etkileşime girebilir.

Hata Yakalama (Error Handling): Yeterli geçmiş verisi olmayan (yeni halka arz) hisselerde sistem çökmez, kullanıcıya bilgilendirici uyarı mesajı döndürür.

🛠️ Kullanılan Teknolojiler
Dil: Python 3.x

API Entegrasyonları:

pyTelegramBotAPI (Telegram Haberleşmesi)

google-genai (Google Gemini AI Karar Motoru)

yfinance (Canlı Borsa Verisi ve Şirket Haberleri)

Veri Analizi: pandas, pandas-ta

Dağıtım (Deployment): Railway (veya benzeri bulut platformları)

📋 Kurulum ve Çalıştırma
Projeyi kendi ortamınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

1. Repoyu Klonlayın

Bash
git clone https://github.com/mstekinn/bist-telegram-bot.git
cd repo-adi

2. Gerekli Kütüphaneleri Yükleyin

Bash
pip install -r requirements.txt
(Eğer gereksinim dosyası yoksa: pip install pyTelegramBotAPI yfinance google-genai pandas-ta)

3. Çevresel Değişkenleri (Environment Variables) Ayarlayın
Sistemin çalışması için sistem ortam değişkenlerine veya bir .env dosyasına aşağıdaki API anahtarlarını ekleyin:

TELEGRAM_TOKEN: BotFather üzerinden aldığınız token.

GEMINI_API_KEY: Google AI Studio'dan aldığınız API anahtarı.

4. Yetkili Kullanıcıyı Belirleyin
bot.py dosyası içindeki YETKILI_KULLANICILAR listesine kendi Telegram ID numaranızı ekleyin.

5. Botu Başlatın

Bash
python bot.py
🎮 Bot Komutları
/bulten: BIST 30 endeksini asenkron olarak tarar, son 5 günlük fiyat trendlerini ve güncel şirket haberlerini analiz eder. Gemini AI aracılığıyla AL/SAT potansiyeli en yüksek 6 hissenin teknik analiz raporunu sunar.

/analiz [HİSSE_KODU]: Belirtilen hissenin (Örn: /analiz THYAO) 3 aylık geçmiş verisini çeker, RSI ve SMA hesaplamalarını yapar ve AI destekli özel destek/direnç noktalarını belirler.

⚠️ Yasal Uyarı
Bu proje tamamen bir yazılım geliştirme, API entegrasyonu ve yapay zeka demosu amacı taşımaktadır. Bot tarafından üretilen çıktılar matematiksel verilere ve yapay zeka yorumlarına dayanmakta olup, KESİNLİKLE YATIRIM TAVSİYESİ DEĞİLDİR (YTD). Borsa verileri BIST kuralları gereği 15 dakika gecikmeli olabilir.
