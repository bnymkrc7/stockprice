# Bir Aylık Makine Öğrenmesi Öğrenim & Proje Planı
## (PyTorch ile Hisse Senedi Fiyat Tahmini - LSTM & GRU)

**Ana Kaynak:** [Stock Price Prediction with PyTorch (Medium)](https://medium.com/swlh/stock-price-prediction-with-pytorch-37f52ae84632)

---

## 🛠️ Teknik Altyapı & Ortam Hazırlığı (Aşama 0)

**Süre:** ~30-45 dakika

### 0.1 — Sanal Ortam ve GPU Kontrolü

```bash
source .venv/bin/activate
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
```

📌 **Neden GPU Kontrolü?** LSTM/GRU eğitimi GPU'da çok daha hızlı çalışır. CUDA yoksa CPU'ya otomatik fallback yapılır.

### 0.2 — Gerekli Paketler

```bash
pip install yfinance seaborn scikit-learn matplotlib tradingview-screener tradingview-ta rookiepy
pip freeze > requirements.txt
```

| Paket | Kullanım Amacı |
|-------|---------------|
| **yfinance** | Yahoo Finance'dan tarihsel hisse verisi çeker (ücretsiz, API key gerekmez) |
| **seaborn** | Daha güzel grafikler için |
| **scikit-learn** | MinMaxScaler ve metrik hesaplamaları için |
| **tradingview-screener** | (Opsiyonel) TradingView premium verileri için cookie auth |
| **tradingview-ta** | (Opsiyonel) Teknik analiz indikatörleri |

### 0.3 — Klasör Yapısı

```
stock-price-prediction/
├── data/
│   ├── raw/              # Orijinal CSV'ler (yfinance'dan indirilen)
│   └── processed/        # Ölçeklenmiş+pencere uygulanmış tensorler
├── notebooks/            # Jupyter Notebook'lar (ana çalışma alanı)
│   ├── 01_veri_kesfi.ipynb
│   ├── 02_veri_hazirlama.ipynb
│   ├── 03_model_lstm.ipynb
│   ├── 04_model_gru.ipynb
│   └── 05_karsilastirma.ipynb
├── src/                  # Tekrar kullanılabilir Python modülleri
│   ├── data_loader.py    # Veri indirme
│   ├── preprocessing.py  # Ölçekleme, pencereleme
│   ├── models.py         # LSTM & GRU mimarileri
│   ├── train.py          # Eğitim döngüsü
│   └── evaluate.py       # Değerlendirme metrikleri & grafikler
├── outputs/
│   ├── figures/          # Üretilen grafikler
│   └── models/           # Eğitilmiş .pth dosyaları
├── docs/
├── .venv/
├── .gitignore
└── requirements.txt
```

📌 **Neden bu yapı?**
- `src/` modülleri notebook'lardan import edilir → Kod tekrarı olmaz
- İlerde farklı veriyle çalışmak istersen `data_loader.py`'ı değiştirmek yeterli
- `outputs/` klasörü modelleri ve grafikleri düzenli tutar

### 0.4 — .gitignore Dosyası

```
.venv/
data/raw/
data/processed/*.pt
outputs/models/*.pth
__pycache__/
.ipynb_checkpoints/
*.pyc
```

---

## 📅 Haftalık Özet Tablosu

| Hafta | Odak Noktası & Faaliyetler | Hafta Sonu Beklenen Çıktı |
| :---: | :--- | :--- |
| **1** | ML temelleri (gözetimli/gözetimsiz, regresyon/sınıflandırma), Python temelleri, Jupyter ve Pandas'a giriş (Bölüm 1). | ML temellerinin kavranması; Python & Jupyter ortamının kurulması; temel veri işleme becerileri. |
| **2** | ML temellerine devam (regresyon, model değerlendirme), Pandas & veri analizi (Bölüm 2), basit regresyon mini egzersizi. | Regresyon ve değerlendirme metrikleri bilgisi; veri işleme için Pandas yetkinliği; tamamlanmış basit bir doğrusal regresyon alıştırması. |
| **3** | PyTorch temelleri (hızlı başlangıç kılavuzu), zaman serisi tahmini ve RNN kavramlarına (LSTM/GRU) giriş. | Temel PyTorch bilgisi (tensorler, eğitim döngüsü); RNN'ler ve sıra (sequence) modelleme hakkında kavramsal anlayış. |
| **4** | Proje uygulaması: veri hazırlama (hisse verileri, ölçekleme, kayan pencere), PyTorch'ta LSTM & GRU modellerinin kurulması. | Veri ön işleme ve ilk LSTM/GRU model tanımlamaları için özgün kodlar; modelleri eğitmeye hazır hale gelme. |
| **5** | Proje eğitimi ve testi: LSTM ve GRU modellerinin eğitilmesi, hiperparametre ayarları, metriklerin takibi. | Eğitilmiş LSTM ve GRU modelleri; ilk değerlendirme metrikleri (MSE/RMSE); aşırı öğrenme (overfitting) veya diğer sorunların tespiti. |
| **6** | Model değerlendirme & karşılaştırma, son iyileştirmeler, dokümantasyon ve kapanış. | Nihai model değerlendirmesi (LSTM vs GRU karşılaştırması); temizlenmiş Jupyter Notebook; GitHub için README ve dokümantasyon. |

---

## 📑 Aşamalı Detaylı Plan

### Aşama 1: ML & Veri Bilimi Temelleri (1. ve 2. Haftalar)
**Hedef:** Veri analizi ve ML için gerekli olan temel makine öğrenmesi kavramlarını ve temel araçları (Python, Jupyter, Pandas) öğrenmek.

#### 1. Hafta: ML Kavramlarına Giriş & Python
* **1. Gün: Kurulum ve Oryantasyon:**
  - Sanal ortamı kur ve aktif et: `python -m venv .venv && source .venv/bin/activate`
  - Gerekli paketleri kur: `pip install jupyter pandas numpy matplotlib seaborn scikit-learn`
  - Jupyter Notebook temel kullanımını öğren (hücre çalıştırma, markdown yazımı, `%matplotlib inline`)
  - GPU kontrolü yap: `python -c "import torch; print(torch.cuda.is_available())"`
* **2. Gün: Makine Öğrenmesi Nedir?:** Google'ın "What is ML?" kılavuzlarını okuyarak modellerin verideki kalıpları nasıl öğrendiğini kavrayın. Temel terimleri (veri kümesi, model, eğitim, tahmin) ve gözetimli (supervised) vs. gözetimsiz (unsupervised) öğrenme farklarını öğrenin.
* **3-5. Günler: Temel ML Kursu Modülleri:** Yapay zeka ve makine öğrenmesi üzerine temel regresyon kavramlarını çalışın. Hafta bittiğinde regresyonun ne olduğunu, eğitim/test veri bölünmesini (train/test split) ve RMSE gibi temel metriklerin neyi ifade ettiğini açıklayabilmelisiniz.

#### 2. Hafta: Regresyon, Veri İşleme ve Pandas
* **6. Gün: Regresyon ve Sınıflandırma Metrikleri:** Doğrusal ve doğrusal olmayan regresyon modellerini inceleyin. Model değerlendirmede kullanılan Ortalama Kare Hata (MSE) ve Kök Ortalama Kare Hata (RMSE) kavramlarına odaklanın, çünkü projemizde doğruluğu ölçmek için bunları kullanacağız.
* **7-8. Günler: Python ile Veri Analizi (Pandas):** Veri işleme konusunda uzmanlaşmak için Pandas kütüphanesini çalışın. CSV yükleme (`pd.read_csv`), DataFrame inceleme, eksik verilerle başa çıkma, veri filtreleme ve temel istatistikleri hesaplama konularını öğrenin. Jupyter Notebook üzerinde küçük bir CSV dosyası ile pratik yapın.
* **9-10. Günler: Regresyon Mini Alıştırması:**
  - Scikit-learn ile basit doğrusal regresyon modeli kurun (örneğin ev fiyatları tahmini)
  - Veriyi train/test olarak bölün (`train_test_split`)
  - Modeli eğitin, test kümesinde tahmin yapın
  - MSE ve RMSE değerlerini hesaplayın
  - **Not:** Bu alıştırma için `src/` modülleri oluşturun — proje için modüler yapı alışkanlığı kazanın.
* **1. Aşama Dönüm Noktası:** Katılımcı temel ML kavramlarını anlar ve Python ile basit veri analizi yapabilir. *Çıktı:* Pandas pratik notebookları ve tamamlanmış basit bir regresyon alıştırması.

---

### Aşama 2: PyTorch & Zaman Serisi Proje Uygulaması (3. ve 4. Haftalar)
**Hedef:** Teoriden pratiğe geçiş yaparak PyTorch öğrenmek ve hisse senedi fiyat tahmini projesine başlamak. Derin öğrenme temellerini edinmek ve LSTM/GRU modellerini oluşturmak.

#### 3. Hafta: PyTorch Temelleri & RNN Kavramları
* **11-12. Günler: PyTorch Hızlı Başlangıç:** Resmi PyTorch "Learn the Basics" kılavuzunu takip edin. Tensorler, veri yükleyiciler (Dataset & DataLoader), basit bir model tanımlama, eğitim döngüsü yazma ve modeli değerlendirme adımlarını kodlayarak öğrenin.
* **13. Gün: Zaman Serileri & RNN Giriş:** Zaman serisi tahmini ve Tekrarlayan Sinir Ağları (RNN) teorisini okuyun. Stok fiyatlarının neden zaman serisi olduğunu ve LSTM ile GRU'nun geçmiş bilgileri (hafızayı/gizli durumları) nasıl tuttuğunu kavramsal olarak öğrenin.
* **14-15. Günler: Proje Yaklaşımını Planlama:**
  * **Veri Kümesi:** **`yfinance` ile Amazon (AMZN) hissesi** — 2015-2025 arası günlük veri.
  * **Veri Kaynağı Neden yfinance?** Kaggle yerine yfinance tercih edilir çünkü:
    - Ücretsiz, API key gerekmez
    - 10+ yıllık tarihsel OHLCV verisi çeker
    - TradingView'dan daha uygun (screener anlık snapshot verir, tarihsel seri vermez)
  * **Veri Hazırlama Stratejisi:** Kapanış fiyatını ("Close") normalize etmek (MinMaxScaler ile [-1, 1] arasına, veri sızıntısını engellemek için fit işlemi sadece train verisi üzerinde yapılmalıdır) ve kayan pencere (sliding window) yöntemiyle (örneğin geçmiş 20 günü kullanarak 21. günü tahmin etmek) veri hazırlama fonksiyonunu tasarlayın.
  * **Scaler Kaydı:** `scaler.pkl` ve işlenmiş tensorler `amzn_processed.pt` olarak `data/processed/` altına kaydedilecek.
  * **Ortam Kontrolü:** Seçtiğiniz hisse senedi verisini Pandas ile yükleyip grafiğini çizmeyi deneyin.
  * **Modüler Kod:** `src/data_loader.py`, `src/preprocessing.py`, `src/models.py`, `src/train.py`, `src/evaluate.py` modüllerini oluştur.

#### 4. Hafta: Proje Uygulaması - Veri Hazırlama & Modelleme
* **16-17. Günler: Veri Toplama ve Hazırlama:**
  - `yfinance` ile AMZN verisini indirin ve `data/raw/AMZN_2015-2025.csv` olarak kaydedin.
  - Kapanış fiyatını görselleştirin (20/50 günlük SMA ile).
  - Kayan pencere fonksiyonunu yazarak veriyi girdi dizilerine (sequence) dönüştürün.
  - Veriyi %80 eğitim, %20 test olarak bölün ve bunları PyTorch Tensor'lerine (`torch.from_numpy`) dönüştürün.
  - **Scaler'ı kaydedin:** `pickle.dump(scaler, open("data/processed/scaler.pkl", "wb"))`
* **18-19. Günler: PyTorch'ta LSTM ve GRU Modellerini Tanımlama:**
  - `nn.Module` sınıfından türeterek `LSTMModel` ve `GRUModel` sınıflarını `src/models.py` içinde yazın.
  - Modellerin **2 katmanlı** (layer) ve **hidden_size=50** olmasını sağlayın.
  - **Dropout=0.2** ekleyin (overfitting önleme).
  - Kayıp fonksiyonu: `nn.MSELoss`, Optimizer: `torch.optim.Adam`.
  - **Hiperparametreler:**
    | Parametre | Önerilen Değer | Alternatif Denemeler |
    |-----------|----------------|---------------------|
    | lookback | 20 | 10, 30, 50 |
    | hidden_size | 50 | 32, 64 |
    | num_layers | 2 | 1, 3 |
    | dropout | 0.2 | 0.1, 0.3 |
    | epochs | 100 | 50, 200 |
    | learning_rate | 0.001 | 0.0001, 0.01 |
* **20. Gün: Eğitim Döngüsünü Başlatma:**
  - İlk model (örn. LSTM) için eğitim döngüsünü `src/train.py` içinde yazın.
  - Her epoch'ta ileri besleme, loss hesaplama, geri yayılım (`loss.backward()`), ağırlık güncelleme (`optimizer.step()`).
  - **Dikkat:** Her epoch'ta `optimizer.zero_grad()` ile gradyanları sıfırlayın.
  - Kaybın düştüğünü doğrulayın ve `loss_history` listesine kaydedin.
  - **GPU Fallback:** `device = "cuda" if torch.cuda.is_available() else "cpu"` ile otomatik seçim.

---

### Aşama 3: Model Eğitimi, Değerlendirme & Belgelendirme (5. ve 6. Haftalar)
**Hedef:** Modellerin eğitimini tamamlamak, LSTM ile GRU performanslarını karşılaştırmak ve projeyi tüm çıktılarıyla son haline getirmek.

#### 5. Hafta: Model Eğitimi ve Değerlendirme
* **21-22. Günler: Modellerin Eğitilmesi:** LSTM ve GRU modellerinin ikisini de aynı veriler ve hiperparametrelerle eğitin. Eğitim sürelerini (kronometre kullanarak) ölçün. Aşırı öğrenme (overfitting) belirtilerini izleyin.
* **23. Gün: Model Performansının Değerlendirilmesi:**
  - Test verisi üzerinde modelleri test edin.
  - **Metrikler:**
    - **MSE:** Ortalama Kare Hata (büyük hataları cezalandırır)
    - **RMSE:** Kök Ortalama Kare Hata (dolar cinsinden hata — yorumlanabilir)
  - Gerçek fiyatlar ile tahminleri aynı grafik üzerinde çizdirin.
  - **Scaler'ı geri çevir:** Tahmin edilen scaled veriyi `scaler.inverse_transform()` ile dolar cinsine çevirin.
  - **Not:** Genelde GRU daha hızlı eğitilir ve LSTM'e yakın/benzer doğruluk sunar.
* **24. Gün: Hiperparametre İyileştirmeleri:** Sonuçlar yetersizse pencere boyutunu (lookback window), katman sayısını veya epoch sayısını değiştirerek iyileştirmeler yapmayı deneyin. overfitting'i önlemek için Dropout eklemeyi araştırın.

#### 6. Hafta: Proje Kapanışı - Raporlama & Sunum
* **25-26. Günler: Kod Düzenleme ve Yorumlar:** Jupyter Notebook'taki kodları düzenleyin, gereksiz deneme çıktılarını silin. Veri Yükleme, Ön İşleme, Model Tanımlama, Eğitim ve Değerlendirme başlıkları altında düzenli Markdown hücreleri oluşturun.
* **27. Gün: Dokümantasyon (README & Rapor):**
  - GitHub projesi için `README.md` oluşturun.
  - **İçerik:**
    - Proje özeti ve amacı
    - Kurulum talimatları (`pip install -r requirements.txt`)
    - Çalıştırma talimatları (`jupyter notebook` ve notebook'ları sırayla aç)
    - Kullanılan mimariler (LSTM/GRU) ve parametreler
    - Elde edilen sonuçlar (grafikler, MSE/RMSE tabloları)
    - TradingView entegrasyonu (opsiyonel ise belirtin)
  - `.gitignore` dosyasını kontrol edin (`.venv/`, `data/raw/`, `*.pth`, `__pycache__/` hariç).
* **28-30. Günler: Kritik Düşünce ve Son Kontroller:** Projeyi baştan sona hatasız çalıştığını doğrulamak için yeniden başlatıp tüm hücreleri sırayla çalıştırın. ML modellerinin finansal tahminlerdeki sınırlarını anlamak adına kritik okumalar yapın (örneğin yapay zekanın karmaşık sosyal alanlardaki tahmin sınırlarına dair eleştirileri inceleyin).

---

## 📦 Teslim Edilecek Çıktılar

| Çıktı | Adet | Açıklama |
|-------|------|----------|
| Python modülleri | 5 | `data_loader.py`, `preprocessing.py`, `models.py`, `train.py`, `evaluate.py` |
| Jupyter Notebook | 5 | `01_veri_kesfi` → `05_karsilastirma` |
| Eğitilmiş model | 2 | `lstm_epoch100.pth`, `gru_epoch100.pth` |
| Karşılaştırma raporu | 1 | Tablo + grafik (MSE, RMSE, süre, parametre sayısı) |
| Grafik dosyası | 3+ | `predictions.png`, `loss.png`, `comparison.png` |
| README | 1 | Proje dokümantasyonu |
| requirements.txt | 1 | Tüm bağımlılıklar |
| .gitignore | 1 | `.venv/`, `data/raw/`, `*.pth`, `__pycache__/` hariç |

---

## 🎁 Opsiyonel İleri Seviye Özellikler (İsteğe Bağlı)

### TradingView Entegrasyonu

**Amaç:** Model tahminlerine teknik analiz indikatörleri (RSI, MACD, SMA) ek feature olarak eklemek.

**Gereksinimler:**
- TradingView hesabı (ücretsiz)
- `tradingview-screener` ve `tradingview-ta` paketleri
- `rookiepy` ile Chrome cookie export

**Kullanım:**

```python
from tradingview_screener import Query
import rookiepy

try:
    # Linux üzerinde Snap veya Gnome Keyring kısıtlamaları nedeniyle hata verebilir
    cookies = rookiepy.to_cookiejar(rookiepy.chrome(['.tradingview.com']))
except Exception as e:
    # Keyring/Snap hatası durumunda tarayıcıdan manuel alınan sessionid yedeğine geçin:
    print(f"rookiepy hata verdi: {e}. Manuel sessionid yedeğine geçiliyor...")
    cookies = {'sessionid': '<tarayıcıdan_kopyalanan_sessionid_değeri>'}

total, df = Query().get_scanner_data(cookies=cookies)
```

**Not:** Bu özellik **opsiyoneldir**. Temel proje `yfinance` ile tamamlanabilir. TradingView sadece ek feature engineering için kullanılabilir.

---

## ⚠️ Kritik Uyarılar & İpuçları

1. **Scaler Kaydı:** Model eğitildikten sonra yeni veri üzerinde tahmin yapmak için `scaler.pkl` kaydedilmeli. Tahmin sonrası `inverse_transform()` ile dolar cinsine çevrilmeli.

2. **GPU Fallback:** `torch.cuda.is_available()` kontrolü yapın. CUDA yoksa otomatik olarak CPU'ya geçin.

3. **Overfitting Önleme:**
   - Dropout kullanın (0.2 önerilir)
   - Erken durdurma (early stopping) uygulayın (validation loss artmaya başlarsa dur)
   - Eğitim/test verisi ayrımını koruyun (test verisini asla eğitimde kullanmayın)

4. **Modüler Kod:** Tüm fonksiyonları `src/` modüllerine yazın. Notebook'larda sadece import ve çağırma olsun.

5. **Versiyon Kontrolü:** `.gitignore` ile `.venv/`, `data/raw/`, `*.pth` gibi büyük/dinamik dosyaları hariç tutun.

6. **Hata Ayıklama:**
   - `optimizer.zero_grad()` her epoch'ta çağrılmalı
   - Tensor boyutlarını kontrol edin (`print(x.shape)`)
   - CUDA kullanıyorsanız `.to(device)` ile tüm tensorleri modele gönderin

---

## 📚 Ek Kaynaklar

| Konu | Kaynak |
|------|--------|
| PyTorch Temelleri | [Official PyTorch Tutorial](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) |
| LSTM/GRU Teorisi | [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) |
| Zaman Serisi | [Time Series Forecasting with PyTorch](https://pytorch.org/tutorials/intermediate/time_series_forecasting_tutorial.html) |
| yfinance | [yfinance Documentation](https://pypi.org/project/yfinance/) |
| Scikit-learn | [Scikit-learn Documentation](https://scikit-learn.org/stable/) |
