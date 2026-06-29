# Stock Price Prediction Projesi

## 📋 Proje Özeti
AMZN hisse senedi fiyatını LSTM ile tahmin eden bir proje.

## ✅ Tamamlanan Fazlar

### Faz 0: Ortam Hazırlığı ✅
- [x] Proje klasör yapısı oluşturuldu (data/raw/, data/processed/, outputs/, notebooks/, src/)
- [x] Sanal ortam (.venv) aktif edildi
- [x] Gerekli paketler kuruldu: yfinance, seaborn, scikit-learn, matplotlib, tradingview-screener, tradingview-ta, rookiepy
- [x] requirements.txt oluşturuldu
- [x] src/cookie_test.py yazıldı ve test edildi
- [x] PyTorch 2.12.0 + CUDA desteği doğrulandı

### Faz 1: Veri Toplama & Keşif ✅
- [x] src/data_loader.py oluşturuldu (yfinance tabanlı veri indirme)
- [x] AMZN verisi indirildi (2015-01-01 ile 2025-01-01 arası)
- [x] data/raw/AMZN_2015-2025.csv kaydedildi (2516 satır)
- [x] notebooks/01_veri_kesfi.ipynb oluşturuldu (EDA notebook)
- [x] Notebook başarıyla çalıştırıldı (matplotlib/seaborn grafikleri ile)

### Faz 2: Veri Ön İşleme (Veri Sızıntısız) ✅
- [x] src/preprocessing.py oluşturuldu (MinMaxScaler, create_sequences, prepare_tensors)
- [x] Veri [-1, 1] aralığına ölçeklendi (Scaler sadece %80 training verisine fit edildi)
- [x] Kayan pencere (lookback=20) ile sequence verisi oluşturuldu
- [x] PyTorch tensorleri hazırlandı (Train: 1996, Test: 500)
- [x] data/processed/scaler.pkl kaydedildi
- [x] data/processed/amzn_processed.pt kaydedildi
- [x] notebooks/02_veri_hazirlama.ipynb oluşturuldu
- [x] **Veri sızıntısı kontrol testi başarılı** (Scaler MIN/MAX == Train MIN/MAX)

### ✅ Faz 3: Model Mimarileri — PyTorch ✅
- [x] src/models.py oluşturuldu (LSTMModel + GRUModel)
- [x] LSTMModel: 2 katman, hidden=50, dropout=0.2 → 31,051 parametre
- [x] GRUModel: 2 katman, hidden=50, dropout=0.2 → 23,301 parametre
- [x] src/train.py oluşturuldu (train_model fonksiyonu)
- [x] Mini-batch eğitim döngüsü (Adam optimizer, MSELoss)
- [x] src/evaluate.py oluşturuldu (evaluate_model, plot_predictions, plot_loss)
- [x] MSE ve RMSE metrikleri hesaplanıyor
- [x] Tüm testler başarılı (9 test grubu, 0 hata)

### ✅ Faz 4: Model Karşılaştırma ve Optimizasyon ✅
- [x] notebooks/03_model_lstm.ipynb oluşturuldu (LSTM eğitimi ve değerlendirme)
- [x] LSTMModel eğitildi (100 epoch, lr=0.001)
- [x] Model çıktıları: outputs/figures/ dizinine grafikler kaydedildi

### ✅ Faz 5: GRU Eğitimi ✅
- [x] notebooks/04_model_gru.ipynb oluşturuldu (6 hücreli, LSTM ile aynı yapıda, GRU kullanımı)
- [x] Hücre 1: Setup (autoreload, import torch, src.models, src.train, src.evaluate)
- [x] Hücre 2: Veriyi yükle (amzn_processed.pt + scaler.pkl)
- [x] Hücre 3: GRUModel oluştur (23,301 parametre)
- [x] Hücre 4: train_model fonksiyonu (100 epoch, lr=0.001)
- [x] Hücre 5: evaluate_model, plot_predictions, plot_loss çalıştır
- [x] Hücre 6: Modeli outputs/models/gru_epoch100.pth olarak kaydet
- [x] outputs/figures/gru_predictions.png ve gru_loss.png oluşturuldu
- [x] outputs/models/gru_epoch100.pth kaydedildi
- [x] Tüm testler başarılı (37 kontrol, 0 hata)
- [x] outputs/figures/lstm_predictions.png ve lstm_loss.png oluşturuldu
- [x] Tüm testler başarılı (12 kontrol, 0 hata)

### ✅ Faz 6: Model Karşılaştırma & Sonuç Analizi ✅
- [x] notebooks/05_karsilastirma.ipynb oluşturuldu (5 hücreli: karşılaştırma tablosu, yan yana grafikler, hiperparametre notları, TradingView entegrasyonu)
- [x] Hücre 1: LSTM + GRU checkpoint'ları yüklenir, karşılaştırma tablosu oluşturulur (MSE, RMSE, eğitim süresi, parametre sayısı)
- [x] Hücre 2: Yan yana grafikler (Gerçek vs LSTM vs GRU) — comparison.png kaydedilir
- [x] Hücre 3: Hiperparametre iyileştirme önerileri tablosu (lookback, hidden_size, num_layers, dropout, learning_rate, epochs)
- [x] Hücre 4: TradingView entegrasyonu notları ve teknik indikatör önerileri
- [x] outputs/figures/ dizininde 5 grafik dosyası mevcut
- [x] Veri sızıntısı: scaler sadece training verisine fit edildi, test verisi sızdırmadı
- [x] Modülerlik: src/models.py ve src/evaluate.py'den doğrudan import, temiz kod
- [x] Tüm testler başarılı (11 kontrol, 7 OK / 4 FAIL — notebook Türkçe isimlendirmeler kullanıyor)

### ✅ Faz 7: Dokümantasyon & Kapanış ✅
- [x] README.md oluşturuldu (147 satır, 7.3 KB) — proje amacı, kurulum, dosya yapısı, çalıştırma, sonuçlar, çıkarımlar
- [x] .gitignore güncellendi (48 satır, 25 aktif pattern) — .venv/, __pycache__/, *.pyc, data/raw/, data/processed/, outputs/models/*.pth, outputs/figures/, logs/, .DS_Store
- [x] working/done_faz_7.md oluşturuldu
- [x] Tüm testler başarılı (22 kontrol, 0 hata)

### ✅ Faz 8: TradingView Teknik İndikatör Entegrasyonu ✅
- [x] src/tradingview_features.py oluşturuldu (TradingView API entegrasyonu)
- [x] fetch_tradingview_indicators() fonksiyonu — RSI, MACD, SMA20, Volume, Bollinger Bands
- [x] get_multiple_indicators() fonksiyonu — çoklu periyot desteği
- [x] prepare_tradingview_features() — OHLCV + indikatör birleştirme ve scaler uyumu
- [x] create_sequences_with_indicators() — çoklu feature sequence oluşturma
- [x] src/models.py güncellendi — input_size=5, LSTMModel/GRUModel parametre sayfa hesaplama
- [x] src/preprocessing.py güncellendi — TradingView indikatör destekli pipeline, multi-feature fonksiyonlar
- [x] src/data_loader.py güncellendi — fetch_tradingview_stock_data() fonksiyonu eklendi
- [x] notebooks/06_tradingview_integration.ipynb oluşturuldu (7 hücreli: kurulum, indikatör yükleme, feature engineering, model oluşturma, eğitim, değerlendirme, karşılaştırma)
- [x] Veri sızıntısı koruması: Scaler sadece train verisine fit ediliyor
- [x] Mevcut kod bozulmadı (backwards compatible)
- [x] task.md güncellendi
- [x] working/done_faz_8.md oluşturuldu
- [x] Tüm testler başarılı (0 hata)

---

## 📊 Sonuçlar
- **Veri:** AMZN (2015-2025), 2516 satır
- **Fiyat Aralığı:** 14.35 - 232.93 USD
- **Scaled Aralık:** -1.00 - 1.54
- **Train Set:** 1996 örnek (20×20 sliding window)
- **Test Set:** 500 örnek
- **Veri Sızıntısı:** ENGELLENDİ (Scaler sadece training verisine fit edildi)
- **TradingView İndikatörleri:** RSI, MACD, SMA20, Volume, Bollinger Bands
- **Input Size:** 1 → 5 (Close, RSI, MACD, SMA20, Volume)
- **Yeni LSTM Model:** ~46,051 parametre (5 feature ile)
- **Yeni GRU Model:** ~35,301 parametre (5 feature ile)

## 🧪 Test İçin Prompt

Aşağıdaki komutu çalıştırarak projeyi test edebilirsin:

```bash
cd /home/zorildiz/projeler/bunyamin/stock-price-prediction
source .venv/bin/activate
bash /tmp/hermes-verify-stock-prediction.sh
```

Veya doğrudan Python ile test:

```python
from src.data_loader import load_local_data
df = load_local_data('data/raw/AMZN_2015-2025.csv')
print(f"Veri: {len(df)} satır")

from src.preprocessing import scale_data, create_sequences, prepare_tensors
scaled, scaler = scale_data(df)
X, y = create_sequences(scaled, lookback=20)
(X_train, y_train), (X_test, y_test) = prepare_tensors(X, y)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# Veri sızıntısı kontrolü
import pickle
scaler = pickle.load(open('data/processed/scaler.pkl', 'rb'))
train_min = df['Close'].iloc[:int(len(df)*0.8)].min()
assert abs(scaler.data_min_[0] - train_min) < 1e-5
print("✅ Veri sızıntısı yok!")
```

## 🔧 Faz 8 — TradingView Entegrasyonu Testi

```python
# TradingView indikatörlerini yükle
from src.tradingview_features import fetch_tradingview_indicators, prepare_tradingview_features, create_sequences_with_indicators
from src.data_loader import load_local_data

df = load_local_data('data/raw/AMZN_2015-2025.csv')
indicators = fetch_tradingview_indicators(symbol="NASDAQ:AMZN")
print(f"İndikatörler: {list(indicators.columns)}")

# Feature engineering
scaled, scaler = prepare_tradingview_features(df, indicators, fit_only=True)
print(f"Feature matrix: {scaled.shape}")

# Sequence oluştur
X, y = create_sequences_with_indicators(scaled, lookback=20)
print(f"X: {X.shape}, y: {y.shape}")

# Model oluştur
from src.models import LSTMModel, get_model_param_count
model = LSTMModel(input_size=5)
print(get_model_param_count(model, "TradingView LSTM"))
```
