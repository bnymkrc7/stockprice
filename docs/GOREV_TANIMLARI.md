# ✅ Hisse Senedi Fiyat Tahmini — Görev Tanımları & Takip

**Proje:** `/home/zorildiz/projeler/bunyamin/stock-price-prediction`
**Detaylı Plan:** `docs/UYGULAMA_PLANI.md` (mentörlük stili)
**Context7 ile doğrulanmıştır:** ✓ yfinance, tradingview-screener, tradingview-ta, PyTorch LSTM/GRU

---

## 🟢 Aşama 0: Ortam Hazırlığı

- [ ] **0.1** Sanal ortamı doğrula: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] **0.2** Paketleri kur: `pip install yfinance seaborn tradingview-screener tradingview-ta rookiepy`
- [ ] **0.3** Klasör yapısını oluştur: `data/raw/ data/processed/ outputs/figures/ outputs/models/`
- [ ] **0.4** `requirements.txt` çıkar
- [ ] **0.5** TradingView cookie setup'ını dene (rookiepy ile Chrome'dan cookie çek)

---

## 🟢 Aşama 1: Veri Toplama & Keşif

### 1.1 `src/data_loader.py`
- [ ] **1.1** `fetch_stock_data()` fonksiyonu (yfinance ile)
- [ ] **1.2** AMZN verisini 2015-2025 indir, `data/raw/` altına kaydet

### 1.2 `notebooks/01_veri_kesfi.ipynb`
- [ ] **1.3** Veriyi yükle ve keşfet: info(), describe(), head(), isnull()
- [ ] **1.4** Grafik: kapanış fiyatı + 20/50 günlük SMA
- [ ] **1.5** Ek keşif: günlük getiri dağılımı, hacim analizi (opsiyonel)

---

## 🟢 Aşama 2: Veri Ön İşleme

### 2.1 `src/preprocessing.py`
- [ ] **2.1** `scale_data()` fonksiyonu (MinMaxScaler, [-1,1])
- [ ] **2.2** `create_sequences()` fonksiyonu (lookback=20)
- [ ] **2.3** `prepare_tensors()` fonksiyonu (train/test split → torch tensors)

### 2.2 `notebooks/02_veri_hazirlama.ipynb`
- [ ] **2.4** Ölçekleme, pencereleme, tensor dönüşümü
- [ ] **2.5** Veriyi ve scaler'ı `data/processed/` altına kaydet

---

## 🟢 Aşama 3: Model Mimarileri

### 3.1 `src/models.py`
- [ ] **3.1** `LSTMModel` sınıfı (2 katman, hidden=50, dropout=0.2)
- [ ] **3.2** `GRUModel` sınıfı (2 katman, hidden=50, dropout=0.2)

### 3.2 `src/train.py`
- [ ] **3.3** `train_model()` fonksiyonu (epoch loop, loss takibi, süre ölçümü)

### 3.3 `src/evaluate.py`
- [ ] **3.4** `evaluate_model()` — MSE/RMSE hesaplama
- [ ] **3.5** `plot_predictions()` — gerçek vs tahmin grafiği
- [ ] **3.6** `plot_loss()` — eğitim loss eğrisi

---

## 🟢 Aşama 4: LSTM Eğitimi

- [ ] **4.1** `notebooks/03_model_lstm.ipynb` oluştur
- [ ] **4.2** Veriyi yükle, modeli kur, MSELoss + Adam optimizer
- [ ] **4.3** Epochs=100 eğitimi çalıştır
- [ ] **4.4** Tahmin grafiği + loss eğrisi çiz
- [ ] **4.5** Modeli `outputs/models/lstm_epoch100.pth` kaydet

---

## 🟢 Aşama 5: GRU Eğitimi

- [ ] **5.1** `notebooks/04_model_gru.ipynb` oluştur
- [ ] **5.2** Aynı parametrelerle GRU eğit (fair comparison)
- [ ] **5.3** Tahmin grafiği + loss eğrisi çiz
- [ ] **5.4** Modeli `outputs/models/gru_epoch100.pth` kaydet

---

## 🟢 Aşama 6: Karşılaştırma & İyileştirme

- [ ] **6.1** `notebooks/05_karsilastirma.ipynb` oluştur
- [ ] **6.2** Karşılaştırma tablosu: MSE, RMSE, süre, parametre sayısı
- [ ] **6.3** Yan yana grafik: Gerçek + LSTM + GRU
- [ ] **6.4** Hiperparametre denemeleri: lookback=10/30/50, hidden=32/64, dropout
- [ ] **6.5** TradingView TA entegrasyonu (opsiyonel): teknik indikatörleri ek feature olarak ekle
- [ ] **6.6** Overfitting analizi & kritik yorum: ML modellerinin finansal tahmin sınırları

---

## 🟢 Aşama 7: Dokümantasyon & Kapanış

- [ ] **7.1** `README.md` yaz: proje özeti, kurulum, çalıştırma, sonuçlar
- [ ] **7.2** `.gitignore` oluştur: `.venv/`, `data/raw/`, `*.pth`, `__pycache__/`
- [ ] **7.3** Tüm notebook'ları temizle: gereksiz çıktıları sil
- [ ] **7.4** Kernel → Restart & Run All ile her şeyi doğrula

---

## 📈 Hedef Çıktılar

| Çıktı | Adet | Açıklama |
|-------|------|----------|
| Python modülleri | 5 | data_loader, preprocessing, models, train, evaluate |
| Jupyter Notebook | 5 | 01_veri_kesfi → 05_karsilastirma |
| Eğitilmiş model | 2 | LSTM + GRU (.pth) |
| Karşılaştırma raporu | 1 | Tablo + grafik |
| Grafik dosyası | 3+ | predictions, loss, comparison |
| README | 1 | Proje dokümantasyonu |
| requirements.txt | 1 | Bağımlılıklar |

---

> ✅ **Kullanım:** Görev tamamlandıkça `[ ]` → `[x]` yap. Her aşamada "Neden böyle yapıyoruz?" sorusunu sor ve plandaki açıklamaları oku. Anlamadığın her şeyi Aura'ya sor — mentörlük modundayız!