# 📋 Hisse Senedi Fiyat Tahmini — Master Görev Takip Listesi (TASKS.md)

Bu liste, yerel Hermes ajanı ile yürüteceğiniz tüm proje fazlarının durumunu takip etmek için tasarlanmıştır. Görevler tamamlandıkça `[ ]` işaretini `[x]` yapabilirsiniz.

---

## 🟢 Faz 0: Ortam Hazırlığı
- [ ] **0.1** Proje ana dizin klasör yapısının oluşturulması (`data/raw`, `data/processed`, `outputs/figures`, `outputs/models`, `notebooks`, `src`)
- [ ] **0.2** Sanal ortam doğrulaması ve paketlerin kurulumu (`yfinance`, `seaborn`, `scikit-learn`, `rookiepy`, `tradingview-ta`, `tradingview-screener`)
- [ ] **0.3** Bağımlılıkların dökümünün alınması (`requirements.txt`)
- [ ] **0.4** `src/cookie_test.py` dosyasının hata yakalama/yedek mekanizmasıyla yazılması ve doğrulanması

## 🟢 Faz 1: Veri Toplama & Keşif ✅ TAMAMLANDI
- [x] **1.1** `src/data_loader.py` modülünün (MultiIndex sütun düzleştirme fonksiyonlu) oluşturulması
- [x] **1.2** AMZN hissesi 2015-2025 verisinin indirilip `data/raw/` altına kaydedilmesi
- [x] **1.3** `notebooks/01_veri_kesfi.ipynb` oluşturulması ve EDA işlemlerinin çalıştırılması
- [x] **1.4** Trend SMA grafikleri (20/50 SMA) ve günlük getiri histogramının çizdirilmesi

## 🟢 Faz 2: Veri Ön İşleme
- [ ] **2.1** `src/preprocessing.py` modülünün yazılması (MinMaxScaler fit işleminin sadece train setine yapılması ve test verisinin sızdırılmaması)
- [ ] **2.2** Kayan pencere (`lookback=20`) ve sequence oluşturma fonksiyonunun yazılması
- [ ] **2.3** `prepare_tensors` ile verilerin PyTorch float tensorlerine çevrilip bölünmesi
- [ ] **2.4** `notebooks/02_veri_hazirlama.ipynb` ile verilerin ve scaler nesnesinin kaydedilmesi (`data/processed/`)
- [ ] **2.5** Veri sızıntısı (Data Leakage) doğrulama testinin çalıştırılması

## 🟢 Faz 3: Model Mimarileri & Eğitim Modülleri
- [ ] **3.1** `src/models.py` içinde 2 katmanlı, hidden=50, dropout=0.2 olan `LSTMModel` ve `GRUModel` sınıflarının tanımlanması
- [ ] **3.2** `src/train.py` içinde Adam + MSELoss kullanan GPU/CPU uyumlu `train_model` eğitim modülünün yazılması
- [ ] **3.3** `src/evaluate.py` içinde inverse_transform özellikli değerlendirme ve grafik çizim modüllerinin yazılması
- [ ] **3.4** Modüllerin sahte (dummy) veriyle test edilmesi (forward ve 5-epoch train testleri)

## 🟢 Faz 4: LSTM Modelinin Eğitimi
- [ ] **4.1** `notebooks/03_model_lstm.ipynb` oluşturulması ve işlenmiş verilerin yüklenmesi
- [ ] **4.2** `LSTMModel` modelinin 100 epoch boyunca eğitilmesi
- [ ] **4.3** Test setinde tahmin yapılması, RMSE skorunun hesaplanması
- [ ] **4.4** Tahmin ve loss grafiklerinin üretilip kaydedilmesi
- [ ] **4.5** Model ağırlıklarının ve metriklerinin `outputs/models/lstm_epoch100.pth` olarak kaydedilmesi

## 🟢 Faz 5: GRU Modelinin Eğitimi
- [ ] **5.1** `notebooks/04_model_gru.ipynb` oluşturulması ve işlenmiş verilerin yüklenmesi
- [ ] **5.2** `GRUModel` modelinin adil karşılaştırma şartlarında 100 epoch eğitilmesi
- [ ] **5.3** Test setinde tahmin yapılması, RMSE skorunun hesaplanması
- [ ] **5.4** Tahmin ve loss grafiklerinin üretilip kaydedilmesi
- [ ] **5.5** Model ağırlıklarının ve metriklerinin `outputs/models/gru_epoch100.pth` olarak kaydedilmesi

## 🟢 Faz 6: Karşılaştırma & Raporlama
- [ ] **6.1** `notebooks/05_karsilastirma.ipynb` oluşturulması
- [ ] **6.2** LSTM vs GRU karşılaştırma tablosunun (MSE, RMSE, Süre, Parametre) oluşturulması
- [ ] **6.3** İki modelin tahminlerinin tek grafikte gerçek fiyatlarla karşılaştırılması (`comparison.png`)
- [ ] **6.4** Proje kök dizininde `README.md` ve `.gitignore` dokümanlarının hazırlanması
- [ ] **6.5** Tüm jupyter notebook'ların otomatik nbconvert komutuyla sırayla çalıştırılarak doğrulanması
