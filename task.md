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

## 📊 Sonuçlar
- **Veri:** AMZN (2015-2025), 2516 satır
- **Fiyat Aralığı:** 14.35 - 232.93 USD
- **Scaled Aralık:** -1.00 - 1.54
- **Train Set:** 1996 örnek (20×20 sliding window)
- **Test Set:** 500 örnek
- **Veri Sızıntısı:** ENGELLENDİ (Scaler sadece training verisine fit edildi)

### 🚀 Sıradaki Adım: Faz 4
- [/] Faz 4: Model Eğitimi & Karşılaştırma (devam ediyor)

---

### ✅ Faz 3: Model Mimarileri — PyTorch ✅
- [x] src/models.py oluşturuldu (LSTMModel + GRUModel)
- [x] LSTMModel: 2 katman, hidden=50, dropout=0.2 → 31,051 parametre
- [x] GRUModel: 2 katman, hidden=50, dropout=0.2 → 23,301 parametre
- [x] src/train.py oluşturuldu (train_model fonksiyonu)
- [x] Mini-batch eğitim döngüsü (Adam optimizer, MSELoss)
- [x] src/evaluate.py oluşturuldu (evaluate_model, plot_predictions, plot_loss)
- [x] MSE ve RMSE metrikleri hesaplanıyor
- [x] Tüm testler başarılı (9 test grubu, 0 hata)

---

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
