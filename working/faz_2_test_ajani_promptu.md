# 🧪 TEST AJANI: FAZ_2 — Veri Ön İşleme (Süre: ~2 saat)

## 🎯 TEST VE DOĞRULAMA DETAYLARI (PLANDAN OKUNAN)
> **Ne öğreneceksin:** Zaman serisi verisini LSTM/GRU'ya nasıl hazırlayacağını — ölçekleme, kayan pencere, tensor dönüşümü.

### 🧠 2.1 — Teori: Neden Ön İşleme?

| Adım | Neden Gerekli? |
|------|----------------|
| **Ölçekleme (Scaling)** | LSTM'ler -1 ile +1 arası girdilerle daha iyi çalışır. Ham fiyatlar 50-200 dolar arası, bu büyük değerler gradient patlamasına (exploding gradient) yol açar |
| **Kayan Pencere (Sliding Window)** | LSTM geçmiş `N` günü görüp `N+1`. günü tahmin eder. Geçmiş 20 günü input, 21. günü output yaparız |
| **Train/Test Split** | Modeli gördüğü veride değil, **görmediği** veride test ederiz. Yoksa "ezberleme" (overfitting) olur |

### 🐍 2.2 — Kod: `src/preprocessing.py`

```python
# src/preprocessing.py
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler

def scale_data(df: pd.DataFrame, column: str = "Close",
               train_ratio: float = 0.8,
               feature_range: tuple = (-1, 1)) -> tuple:
    """
    Veriyi [-1, 1] aralığına ölçekler (Veri sızıntısını önlemek için sadece train verisi fit edilir).
    
    Neden MinMaxScaler? StandartScaler normal dağılım varsayar.
    Hisse fiyatları normal dağılmaz, MinMax daha uygun.
    Neden [-1,1]? tanh aktivasyonu [-1,1] çıktı üretir, girdiyle uyumlu.
    """
    split_idx = int(len(df) * train_ratio)
    scaler = MinMaxScaler(feature_range=feature_range)
    
    # Sadece eğitim verisini fit ediyoruz (Veri Sızıntısı / Data Leakage engellemesi!)
    scaler.fit(df[[column]].iloc[:split_idx])
    
    # Tüm veriyi eğittiğimiz scaler ile dönüştürüyoruz
    scaled = scaler.transform(df[[column]])
    return scaled, scaler

def create_sequences(data: np.ndarray, lookback: int = 20) -> tuple:
    """
    Kayan pencere (sliding window) ile X, y oluşturur.
    
    Örnek: lookback=20, data=[1,2,3,...,100]
    X[0] = [1,2,...,20]  → y[0] = 21
    X[1] = [2,3,...,21]  → y[1] = 22
    
    Neden 20 gün? Hisse fiyatında ~1 ay = 20 işlem günü.
    """
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

def prepare_tensors(X: np.ndarray, y: np.ndarray,
                    train_ratio: float = 0.8,
                    device: str = "cpu") -> tuple:
    """
    Train/test split + numpy'den PyTorch tensor'üne dönüşüm.
    
    Neden unsqueeze(-1)? LSTM (batch, seq_len, input_size) boyutunda bekler.
    Bizim input'umuz (batch, 20), (batch, 20, 1) olmalı.
    """
    split = int(len(X) * train_ratio)
    
    X_train = torch.from_numpy(X[:split]).float().unsqueeze(-1)
    y_train = torch.from_numpy(y[:split]).float().unsqueeze(-1)
    X_test  = torch.from_numpy(X[split:]).float().unsqueeze(-1)
    y_test  = torch.from_numpy(y[split:]).float().unsqueeze(-1)
    
    print(f"📊 Veri boyutları:")
    print(f"   X_train: {X_train.shape}  y_train: {y_train.shape}")
    print(f"   X_test:  {X_test.shape}  y_test: {y_test.shape}")
    print(f"   Train/Test oranı: %{train_ratio*100:.0f} / %{(1-train_ratio)*100:.0f}")
    
    return (X_train.to(device), y_train.to(device)), \
           (X_test.to(device), y_test.to(device))
```

### 📓 2.3 — Notebook: `02_veri_hazirlama.ipynb`

```python
%load_ext autoreload
%autoreload 2
import sys; sys.path.append('..')
import pandas as pd
from src.preprocessing import scale_data, create_sequences, prepare_tensors

# Veriyi yükle
df = pd.read_csv("../data/raw/AMZN_2015-2025.csv", index_col=0, parse_dates=True)

# Ölçekle (Train oranına göre veri sızıntısını engelleyecek şekilde fit edilir)
scaled_data, scaler = scale_data(df, column="Close", train_ratio=0.8)
print(f"Ham fiyat aralığı: {df['Close'].min():.2f} - {df['Close'].max():.2f}")
print(f"Ölçeklenmiş aralık: {scaled_data.min():.2f} - {scaled_data.max():.2f}")

# Kayan pencere
lookback = 20
X, y = create_sequences(scaled_data, lookback=lookback)
print(f"Pencere öncesi: {len(scaled_data)} veri noktası")
print(f"Pencere sonrası: {X.shape[0]} örnek, her örnek {lookback} gün")

# Train/test tensorleri
device = "cuda" if torch.cuda.is_available() else "cpu"
(X_train, y_train), (X_test, y_test) = prepare_tensors(X, y, device=device)

# İşlenmiş veriyi kaydet
import pickle
pickle.dump(scaler, open("../data/processed/scaler.pkl", "wb"))
torch.save({
    'X_train': X_train.cpu(), 'y_train': y_train.cpu(),
    'X_test': X_test.cpu(),   'y_test': y_test.cpu(),
}, "../data/processed/amzn_processed.pt")
```

📌 **Dikkat:** `scaler`'ı da kaydediyoruz çünkü tahmin yaparken çıktıyı tekrar dolar cinsine çevirmemiz gerekecek!

---

## 📋 TEST UYGULAMA TALİMATLARI
1. Kodlama aşamasında yazılan/değiştirilen tüm dosyaların yerlerin olduğunu doğrulayın.
2. İlgili test senaryolarını çalıştırın (örneğin import testleri, model ileri besleme testleri veya veri doğrulama testleri).
3. Test çıktılarında herhangi bir `WARNING` veya `HATA` olmadığından emin olun (oturum bulunamadığında graceful fallback kullanın).
4. Test sonuçlarını `working/test_report_faz_2.md` dosyası olarak kaydedin.
5. Başarılı sonuçları Orkestratör Ajanına rapor edin.
