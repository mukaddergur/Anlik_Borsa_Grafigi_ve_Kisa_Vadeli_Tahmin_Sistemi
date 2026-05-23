#  Real-Time Stock Market Dashboard & Short-Term Prediction System

Bu proje; finansal piyasalardan anlık ve geçmiş verileri çekerek dinamik bir dashboard üzerinde görselleştiren, arka planda makine öğrenmesi (Machine Learning) algoritmaları koşturarak kısa vadeli fiyat ve yön tahmini üreten uçtan uca (end-to-end) bir veri bilimi ve analitiği projesidir.

Proje, kurumsal standartlara uygun olarak **modüler bir mimari (modular architecture)** ile tasarlanmıştır.

---

##  Öne Çıkan Özellikler

- **Anlık Veri Akışı (Live Data Ingestion):** `yfinance` API entegrasyonu ile küresel (AAPL, TSLA, NVDA) ve yerel (THYAO.IS, GARAN.IS) piyasalardan saniyelik/dakikalık gerçek verilerin çekilmesi.
- **Otomatik Yenileme (Auto-Refresh):** `streamlit-autorefresh` mekanizması kullanılarak sayfa kasmadan her 60 saniyede bir verilerin ve grafiklerin canlı güncellenmesi.
- **Gelişmiş Feature Engineering:** Ham fiyat verilerinden teknik indikatörlerin (Hareketli Ortalamalar, Volatilite, Hacim Değişimi, Gün İçi Spread) matematiksel olarak türetilmesi.
- **Zaman Serisi Tabanlı ML Modeli:** Zaman sırasını bozmadan veri setini Train/Test olarak ayıran ve `RandomForestRegressor` kullanan tahmin motoru.
- **Dinamik Sinyal Üretimi:** Yapay zekanın tahmin ettiği fiyat ile anlık fiyatı kıyaslayarak yatırımcıya *"Güçlü Yükseliş Beklentisi"*, *"Düşüş Riski Yüksek"* gibi algoritmik sinyaller sunan karar destek yapısı.

---

##  Kullanılan Teknolojiler

- **Arayüz & Dashboard:** Streamlit
- **Veri Analizi & Manipülasyon:** Pandas, NumPy
- **Veri Kaynağı:** Yahoo Finance API (`yfinance`)
- **Veri Görselleştirme:** Plotly (Interactive Candlestick & Scatter Charts)
- **Makine Öğrenmesi:** Scikit-Learn (Random Forest Regressor)

---
## Veri Bilimi ve Model Detayları
### 1. Feature Engineering (Özellik Mühendisliği)
Model sadece ham fiyatlara bakarak ezber yapmaz. Aşağıdaki teknik göstergeleri hesaplayarak trendi ve momentumu anlamlandırır:

Daily_Return: Günlük yüzde değişim.

MA_7, MA_14, MA_30: Kısa ve orta vadeli Basit Hareketli Ortalamalar.

Volatility_7: Fiyatın son 7 gündeki standart sapması (Risk ölçümü).

Volume_Change: İşlem hacmindeki ivmelenme.

Price_Range: Gün içi en yüksek ve en düşük fiyatın kapanışa oranı.

### 2. Model Doğrulama (Validation)
Zaman serisi verilerinde gelecekteki verilerin geçmişe sızmasını (Data Leakage) önlemek için veriler rastgele karıştırılmadan (shuffle=False) kronolojik sırayla:

%80 Eğitim (Train)

%20 Test (Test)

olarak ayrılmıştır.

Model başarısı aşağıdaki metriklerle anlık olarak ölçülmektedir:

MAE (Mean Absolute Error)

RMSE (Root Mean Square Error)

## Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayabilirsiniz:

### 1. Projeyi Klonlayın veya Klasörü Açın
Bash
cd borsa-tahmin-dashboard
### 2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin
Bash
# Windows için
python -m venv venv
.\venv\Scripts\activate
### 3. Gerekli Kütüphaneleri Yükleyin
Bash
pip install -r requirements.txt
### 4. Uygulamayı Başlatın
Bash
streamlit run app.py
Uygulama otomatik olarak tarayıcınızda aşağıdaki adreste açılacaktır:

Plaintext
http://localhost:8501
## Yasal Uyarı
Bu proje tamamen eğitim ve portfolyo amacıyla geliştirilmiştir.

Sistem tarafından üretilen grafikler, tahminler ve sinyaller kesinlikle yatırım tavsiyesi (enstrüman alım/satım yönlendirmesi) niteliği taşımamaktadır.

##  Proje Klasör Yapısı

Proje, kodun okunabilirliğini ve sürdürülebilirliğini artırmak amacıyla tek bir dosya yerine modüler bileşenlere ayrılmıştır:

```text
borsa-tahmin-dashboard/
│
├── app.py                  # Orkestra şefi; arayüzü yönetir ve modülleri birleştirir.
├── requirements.txt        # Projenin bağımlı olduğu kütüphaneler listesi.
│
├── src/                    # Projenin motor odası (Modüller)
│   ├── data_loader.py      # Canlı ve geçmiş finansal verileri çeken fonksiyonlar.
│   ├── indicators.py       # Matematiksel indikatörleri hesaplayan Feature Engineering alanı.
│   ├── model.py            # ML modelini eğiten ve başarı metriklerini ölçen modül.
│   └── charts.py           # Plotly grafik tasarımlarını barındıran görselleştirme katmanı.
│
└── README.md               # Proje dökümantasyonu.