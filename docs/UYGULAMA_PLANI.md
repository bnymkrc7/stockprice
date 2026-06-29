# 📈 Hisse Senedi Fiyat Tahmini — Uygulama Planı (Mentörlük)
## PyTorch ile LSTM & GRU — Adım Adım, Neden-Sonuç Anlatımlı

**Proje:** `/home/zorildiz/projeler/bunyamin/stock-price-prediction`
**Referans Plan:** `docs/ML_Proje_Plani_TR.md`
**Ortam:** Python 3.12 + PyTorch 2.12 + `.venv` (mevcut)

---

## 🧭 Bu Projede Ne Öğreneceksin?

```
Veri Çekme → Veriyi Anlama → Modele Hazırlama → Model Kurma → Eğitme → Değerlendirme
(yfinance)    (Pandas/plot)   (MinMaxScaler,     (PyTorch)    (backprop)   (MSE/RMSE)
                              sliding window)
```

Her adımda **NEDEN** böyle yaptığımızı, alternatiflerin ne olduğunu ve nelere dikkat etmen gerektiğini açıklayacağım.

---

## 📂 Klasör Yapısı

```
stock-price-prediction/
├── data/
│   ├── raw/              # Orijinal CSV'ler (yfinance'dan indirilen)
│   └── processed/        # Ölçeklenmiş+pencere uygulanmış tensorler
├── notebooks/            # Jupyter Notebook'lar (ana çalışma alanın)
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
├── docs/
├── outputs/
│   ├── figures/
│   └── models/
├── .venv/
└── README.md
```

📌 **Neden bu yapı?** `src/` modülleri notebook'lardan import ediyoruz. Böylece:
- Notebook'lar temiz ve kısa kalır
- Kod tekrarı olmaz
- İlerde farklı veriyle çalıştırmak istersen `data_loader.py`'ı değiştirmen yeterli

---

## 🟢 Aşama 0: Ortam Hazırlığı (Süre: ~30 dk)

> **Ne yapacağız:** Sanal ortamın çalıştığını doğrulayacak, eksik kütüphaneleri kuracak, TradingView hesabını yapılandıracak ve proje klasör yapısını oluşturacağız.

### 0.1 — Ortam Doğrulama

```bash
source .venv/bin/activate
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
```

📌 **Neden CUDA kontrolü?** LSTM/GRU eğitimi GPU'da çok daha hızlı çalışır. Eğer CUDA yoksa sorun değil — CPU'da da çalışır, sadece biraz yavaş olur.

### 0.2 — Gerekli Paketler

```bash
pip install yfinance seaborn tradingview-screener tradingview-ta
```

| Paket | Ne işe yarar? | Alternatifi |
|-------|---------------|-------------|
| **yfinance** | Yahoo Finance'dan tarihsel OHLCV verisi çeker (ücretsiz, API key gerekmez) | Alpha Vantage, Polygon.io |
| **seaborn** | Daha güzel grafikler için matplotlib üstüne katman | Plotly, Altair |
| **tradingview-screener** | TradingView hesabınla anlık veri çekmek için (API key gerekmez, cookie ile auth) | - |
| **tradingview-ta** | TradingView'dan teknik analiz indikatörleri almak için | - |

### 0.3 — TradingView Hesap Kurulumu (API Key)

**Önemli:** TradingView'in resmi bir Python API'si yok. Ama TradingView hesabındaki **oturum bilgilerini (cookie)** kullanarak veri çekebiliriz.

**API Key Oluşturma (TradingView Premium):**
1. TradingView.com'a gir ve hesabına **giriş yap** (Chrome'da)
2. Tarayıcıdan cookie'lerini export etmek için `tradingview-screener` + `rookiepy` kullanacağız

```python
# TradingView oturumunu kullanma (opsiyonel, premium özellikler için)
from tradingview_screener import Query
import rookiepy

try:
    # Linux üzerinde Snap kısıtlamaları veya Gnome Keyring kilidi nedeniyle bu kısım hata verebilir
    cookies = rookiepy.to_cookiejar(rookiepy.chrome(['.tradingview.com']))
    print("Cookie'ler tarayıcıdan başarıyla okundu.")
except Exception as e:
    # Keyring/Snap hatası durumunda tarayıcıdan manuel aldığınız sessionid'yi kullanın:
    print(f"rookiepy hata verdi: {e}. Manuel sessionid yedeğine geçiliyor...")
    cookies = {'sessionid': '<tarayıcıdan_kopyalanan_sessionid_değeri>'}

# Artık premium verilere erişimin var
total, df = Query().get_scanner_data(cookies=cookies)
```

📌 **Alternatif:** TradingView hesabın yoksa veya uğraşmak istemezsen, **yfinance** tek başına yeterli. Projenin temelini yfinance ile kur, sonra istersen TradingView'u ek özellik olarak eklersin.

### 0.4 — Klasörleri ve requirements.txt'yi Oluştur

```bash
mkdir -p data/raw data/processed outputs/figures outputs/models
pip freeze > requirements.txt
```

---

## 🟢 Aşama 1: Veri Toplama ve Keşif (Süre: ~2-3 saat)

> **Ne öğreneceksin:** yfinance ile gerçek dünya finansal verisi çekmeyi, Pandas ile veriyi keşfetmeyi, zaman serisi görselleştirmeyi.

### 📘 1.1 — Veri Kaynağına Karar Verme

**Ana Veri:** `yfinance` ile **AMZN (Amazon)** hissesi, 2015-2025 arası günlük veri.

📌 **Neden AMZN?**
- Likit bir hisse, verisi temiz
- 10 yıllık veri iyi bir eğitim seti
- İstersen sonra AAPL, GOOGL, TSLA ile değiştirebilirsin

📌 **Neden yfinance (TradingView değil)?**
- TradingView screener anlık snapshot verir, **tarihsel zaman serisi vermez**
- yfinance 10+ yıllık OHLCV verisini 1 satır kodla çeker
- yfinance ücretsiz, API key gerekmez

**Ek Veri (Opsiyonel):** TradingView hesabınla `tradingview-ta` kullanarak teknik analiz indikatörleri (RSI, MACD, SMA) çekip modeline ek girdi olarak verebilirsin (Aşama 5'te).

### 🐍 1.2 — Kod: `src/data_loader.py`

```python
# src/data_loader.py
import yfinance as yf
import pandas as pd
from pathlib import Path

def fetch_stock_data(ticker: str = "AMZN",
                     start: str = "2015-01-01",
                     end: str = "2025-01-01",
                     save_path: str = None) -> pd.DataFrame:
    """
    yfinance ile hisse senedi verisi indirir.
    
    Neden yfinance? Yahoo Finance'in ücretsiz API'sini kullanır.
    Dönen sütunlar: Open, High, Low, Close, Volume
    """
    print(f"📥 {ticker} verisi indiriliyor ({start} - {end})...")
    df = yf.download(ticker, start=start, end=end, progress=True)
    
    # MultiIndex sütunları düzleştir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    print(f"✅ {len(df)} satır veri indirildi")
    print(f"   Sütunlar: {list(df.columns)}")
    print(f"   Tarih aralığı: {df.index[0]} → {df.index[-1]}")
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path)
        print(f"💾 Kaydedildi: {save_path}")
    
    return df

def load_local_data(path: str) -> pd.DataFrame:
    """Daha önce kaydedilmiş CSV'yi yükler (tekrar indirmek yerine)"""
    return pd.read_csv(path, index_col=0, parse_dates=True)
```

📌 **Dikkat:** yfinance bazen MultiIndex döndürür. `df.columns.get_level_values(0)` ile düzleştiriyoruz.

### 📓 1.3 — Notebook: `01_veri_kesfi.ipynb`

Bu notebook'ta şunları yapacaksın:

**Hücre 1:** Veriyi yükleme
```python
%load_ext autoreload
%autoreload 2
import sys; sys.path.append('..')
from src.data_loader import fetch_stock_data

df = fetch_stock_data("AMZN", "2015-01-01", "2025-01-01", "data/raw/AMZN_2015-2025.csv")
```

**Hücre 2:** Veriyi tanıma
```python
df.info()           # Veri tipi, null değer var mı?
df.describe()       # İstatistiksel özet (min, max, ortalama)
df.head()           # İlk 5 satır
df.isnull().sum()   # Eksik veri kontrolü
```

📌 **Neden `df.describe()`?** Verinin dağılımını anlamak için. Örneğin Close fiyatı 50-200 dolar arasında mı, uç değerler var mı?

**Hücre 3:** Temel grafik
```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

plt.figure(figsize=(14, 6))
plt.plot(df.index, df['Close'], label='Kapanış Fiyatı', linewidth=1)
plt.plot(df.index, df['Close'].rolling(20).mean(), label='20 Günlük SMA', alpha=0.7)
plt.plot(df.index, df['Close'].rolling(50).mean(), label='50 Günlük SMA', alpha=0.7)
plt.title('Amazon (AMZN) Hisse Fiyatı')
plt.xlabel('Tarih')
plt.ylabel('Fiyat ($)')
plt.legend()
plt.show()
```

📌 **Neden hareketli ortalama?** Zaman serisindeki trendi görmek için. Kısa vadeli dalgalanmaları yumuşatır. Modelimiz de benzer "geçmişe bakma" mantığıyla çalışacak.

**Hücre 4:** Ek keşif (opsiyonel)
```python
# Günlük getiri (return) hesapla
df['Return'] = df['Close'].pct_change()
df['Return'].hist(bins=50, figsize=(10, 4))
plt.title('Günlük Getiri Dağılımı')

# Hacim analizi
df['Volume'].plot(figsize=(14, 3), title='İşlem Hacmi')
```

---

## 🟢 Aşama 2: Veri Ön İşleme (Süre: ~2 saat)

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

## 🟢 Aşama 3: Model Mimarileri — PyTorch (Süre: ~2-3 saat)

> **Ne öğreneceksin:** PyTorch'ta `nn.Module` ile özel model tanımlamayı, LSTM vs GRU farkını, eğitim döngüsünü.

### 🧠 3.1 — Teori: LSTM vs GRU Nedir?

```
RNN (Basit):
  h(t) = tanh(W·x(t) + U·h(t-1))
  ❌ Uzun vadeli bağımlılıkları hatırlayamaz (vanishing gradient)

LSTM (1997):
  + Forget Gate: neyi unutacağını öğrenir
  + Input Gate: neyi hatırlayacağını öğrenir  
  + Output Gate: neyi çıktı olarak vereceğini öğrenir
  ✅ Uzun vadeli (100+ adım) hatırlayabilir
  
GRU (2014):
  - LSTM'in basitleştirilmiş hali (3 gate → 2 gate)
  - Daha az parametre → daha hızlı eğitim
  - Çoğu görevde LSTM'e yakın performans
  ✅ "LSTM'in hızlı kardeşi"
```

📌 **Projemizde:** İkisini de eğitip karşılaştıracağız. Hangisi daha iyi? Tahminin nedir? 😉

### 🐍 3.2 — Kod: `src/models.py`

```python
# src/models.py
import torch.nn as nn

class LSTMModel(nn.Module):
    """
    2 katmanlı LSTM modeli.
    
    Mimarisi:
      Input (batch, 20, 1) 
        → LSTM(hidden=50, layers=2, dropout=0.2) 
        → Linear(50 → 1)
        → Output (batch, 1)
    
    Neden 2 katman? Daha fazla öğrenme kapasitesi.
    Neden dropout=0.2? Overfitting'i önlemek için (nöronların %20'sini rastgele kapatır).
    Neden hidden=50? 20 günlük girdi için yeterli kapasite.
    """
    def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        # x shape: (batch, 20, 1)
        out, _ = self.lstm(x)
        # out shape: (batch, 20, 50) → son adımı al
        return self.fc(out[:, -1, :])
        # çıktı: (batch, 1) — tahmin edilen fiyat

class GRUModel(nn.Module):
    """
    2 katmanlı GRU modeli — LSTM ile aynı parametrelerde.
    """
    def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])
```

📌 **Neden `batch_first=True`?** Girdi boyutu (batch, seq, features) olur. Daha doğal. False olsa (seq, batch, features) olurdu.

📌 **Neden `out[:, -1, :]`?** LSTM her adımda çıktı üretir (20 adım). Son adımın çıktısını alırız çünkü sadece 21. günü tahmin edeceğiz.

### 🐍 3.3 — Kod: `src/train.py`

```python
# src/train.py
import time
import torch
import torch.nn as nn

def train_model(model, X_train, y_train, epochs=100, lr=0.001,
                device="cpu", verbose=True):
    """
    Standart PyTorch eğitim döngüsü.
    
    Adımlar:
    1. forward pass (tahmin yap)
    2. loss hesapla (tahmin ile gerçek arasındaki fark)
    3. backward pass (gradyan hesapla)
    4. optimizer.step() (ağırlıkları güncelle)
    """
    model = model.to(device)
    X_train, y_train = X_train.to(device), y_train.to(device)
    
    criterion = nn.MSELoss()
    # Neden Adam? Adaptive learning rate, genelde SGD'den iyi çalışır
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    loss_history = []
    start_time = time.time()
    
    for epoch in range(epochs):
        model.train()
        
        # Forward
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        
        # Backward
        optimizer.zero_grad()  # Önceki gradyanları sıfırla
        loss.backward()        # Gradyanları hesapla
        optimizer.step()       # Ağırlıkları güncelle
        
        loss_history.append(loss.item())
        
        if verbose and (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] Loss: {loss.item():.6f}")
    
    elapsed = time.time() - start_time
    print(f"✅ Eğitim tamamlandı! Süre: {elapsed:.2f} sn")
    print(f"   Son Loss: {loss_history[-1]:.6f}")
    
    return loss_history, elapsed
```

📌 **Dikkat:** `optimizer.zero_grad()` çok önemli! Her epoch'ta gradyanlar birikir, sıfırlamazsan loss hep aynı kalır.

### 🐍 3.4 — Kod: `src/evaluate.py`

```python
# src/evaluate.py
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def evaluate_model(model, X_test, y_test, scaler=None, device="cpu"):
    """
    Modeli test verisinde değerlendirir.
    
    Metrikler:
    - MSE: Ortalama Kare Hata (büyük hataları cezalandırır)
    - RMSE: Karekök MSE (dolar cinsinden hata)
    """
    model.eval()
    X_test, y_test = X_test.to(device), y_test.to(device)
    
    with torch.no_grad():
        predictions = model(X_test)
    
    # CPU'ya al ve numpy'e çevir
    preds = predictions.cpu().numpy()
    actuals = y_test.cpu().numpy()
    
    # Eğer scaler varsa, orijinal fiyata geri çevir
    if scaler:
        preds = scaler.inverse_transform(preds)
        actuals = scaler.inverse_transform(actuals)
    
    # Metrikler
    mse = mean_squared_error(actuals, preds)
    rmse = np.sqrt(mse)
    
    print(f"📊 Model Değerlendirme:")
    print(f"   MSE : {mse:.4f}")
    print(f"   RMSE: {rmse:.4f} $")
    
    return preds, actuals, mse, rmse

def plot_predictions(actuals, preds, title="Gerçek vs Tahmin", save_path=None):
    """Gerçek fiyatlar ile tahminleri karşılaştırmalı gösterir."""
    plt.figure(figsize=(14, 5))
    plt.plot(actuals, label='Gerçek Fiyat', linewidth=1.5, alpha=0.8)
    plt.plot(preds, label='Tahmin', linewidth=1.5, alpha=0.8)
    plt.title(title)
    plt.xlabel('Gün')
    plt.ylabel('Fiyat ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()

def plot_loss(loss_history, title="Eğitim Kaybı", save_path=None):
    """Loss eğrisini çizer — modelin öğrenip öğrenmediğini gösterir."""
    plt.figure(figsize=(10, 4))
    plt.plot(loss_history, linewidth=1)
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
```

📌 **Loss eğrisi ne anlatır?**
- 📉 **Düzenli düşüyor** → Model öğreniyor ✅
- 📈 **Yükseliyor** → Learning rate çok yüksek, patlıyor
- ➡️ **Düzleşiyor** → Model doyuma ulaştı, daha fazla epoch anlamsız
- 📊 **Train düşer test yükselir** → Overfitting (ezberleme) ⚠️

---

## 🟢 Aşama 4: LSTM Eğitimi (Süre: ~2-3 saat)

> **Ne yapacağız:** LSTM modelini kur, eğit, değerlendir. İlk gerçek modelin olacak! 🎉

### 📓 Notebook: `03_model_lstm.ipynb`

**Hücre 1:** Setup
```python
%load_ext autoreload
%autoreload 2
import sys; sys.path.append('..')
import torch
import pickle
from src.models import LSTMModel
from src.train import train_model
from src.evaluate import evaluate_model, plot_predictions, plot_loss

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Kullanılan cihaz: {device}")
```

**Hücre 2:** Veriyi yükle
```python
data = torch.load("../data/processed/amzn_processed.pt", weights_only=True, map_location=device)
scaler = pickle.load(open("../data/processed/scaler.pkl", "rb"))

X_train, y_train = data['X_train'], data['y_train']
X_test, y_test = data['X_test'], data['y_test']
```

**Hücre 3:** Modeli oluştur
```python
model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)
print(f"📐 Parametre sayısı: {sum(p.numel() for p in model.parameters()):,}")
```

📌 **Parametre sayısı neden önemli?** Çok parametre = yüksek kapasite ama overfitting riski. 50 hidden × 2 layer LSTM için yaklaşık 40K parametre — bu ölçekte bir veri için makul.

**Hücre 4:** Eğit
```python
loss_history, train_time = train_model(
    model, X_train, y_train,
    epochs=100, lr=0.001, device=device
)
```

**Hücre 5:** Değerlendir
```python
preds, actuals, mse, rmse = evaluate_model(
    model, X_test, y_test, scaler=scaler, device=device
)

plot_predictions(actuals, preds,
    title="LSTM: Amazon Hisse Fiyat Tahmini",
    save_path="../outputs/figures/lstm_predictions.png")

plot_loss(loss_history,
    title="LSTM Eğitim Kaybı",
    save_path="../outputs/figures/lstm_loss.png")
```

**Hücre 6:** Modeli kaydet
```python
torch.save({
    'model_state_dict': model.state_dict(),
    'hidden_size': 50,
    'num_layers': 2,
    'mse': mse,
    'rmse': rmse,
    'train_time': train_time,
}, "../outputs/models/lstm_epoch100.pth")
print(f"💾 Model kaydedildi: outputs/models/lstm_epoch100.pth")
```

---

## 🟢 Aşama 5: GRU Eğitimi (Süre: ~1-2 saat)

> **Ne yapacağız:** Aynı veriyi GRU ile eğit, sonuçları karşılaştırmaya hazırlan.

### 📓 Notebook: `04_model_gru.ipynb`

Aynı LSTM notebook'unun aynısı, sadece:

```python
from src.models import GRUModel  # ← LSTM yerine GRU

model = GRUModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)

# ... eğit, değerlendir, kaydet ...

torch.save({...}, "../outputs/models/gru_epoch100.pth")  # ← farklı isim
```

📌 **Neden aynı parametreler?** Fair comparison (adil karşılaştırma) için. İkisi de aynı koşullarda eğitilmeli ki hangisinin daha iyi olduğunu görebilelim.

---

## 🟢 Aşama 6: Karşılaştırma & İyileştirme (Süre: ~2-3 saat)

> **Ne öğreneceksin:** İki modeli objektif karşılaştırmayı, hiperparametre optimizasyonunu, overfitting tespitini.

### 📓 Notebook: `05_karsilastirma.ipynb`

**Hücre 1:** İki modeli de yükle
```python
lstm_ckpt = torch.load("../outputs/models/lstm_epoch100.pth", weights_only=True)
gru_ckpt = torch.load("../outputs/models/gru_epoch100.pth", weights_only=True)

comparison = pd.DataFrame({
    'Metrik': ['MSE', 'RMSE ($)', 'Eğitim Süresi (sn)', 'Parametre Sayısı'],
    'LSTM': [lstm_ckpt['mse'], lstm_ckpt['rmse'], lstm_ckpt['train_time'], 40401],
    'GRU': [gru_ckpt['mse'], gru_ckpt['rmse'], gru_ckpt['train_time'], 30601],
})
print(comparison.to_string(index=False))
```

**Hücre 2:** Yan yana grafik
```python
# İki tahmini aynı grafikte göster
plt.figure(figsize=(14, 5))
plt.plot(actuals, label='Gerçek', linewidth=2, alpha=0.8)
plt.plot(lstm_preds, label='LSTM Tahmin', linewidth=1.5, alpha=0.7)
plt.plot(gru_preds, label='GRU Tahmin', linewidth=1.5, alpha=0.7)
plt.title('LSTM vs GRU: Amazon Hisse Fiyat Tahmini')
plt.legend()
plt.savefig("../outputs/figures/comparison.png", dpi=150)
```

### 🔧 Hiperparametre İyileştirme (Opsiyonel)

İlk sonuçlar kötüyse dene:

| Parametre | Varsayılan | Dene | Neden? |
|-----------|-----------|------|--------|
| `lookback` | 20 | 10, 30, 50 | Kısa/uzun vadeli trendler |
| `hidden_size` | 50 | 32, 64, 128 | Model kapasitesi |
| `num_layers` | 2 | 1, 3 | Derinlik |
| `dropout` | 0.2 | 0, 0.3, 0.5 | Overfitting kontrolü |
| `learning_rate` | 0.001 | 0.01, 0.0001 | Öğrenme hızı |
| `epochs` | 100 | 50, 200 | Eğitim süresi |

### 🧠 TradingView Entegrasyonu (Ek Özellik)

Modelin tahmin gücünü artırmak için teknik indikatörleri ek girdi olarak kullanabiliriz:

```python
from tradingview_ta import TA_Handler, Interval

# TradingView'dan teknik indikatör al
handler = TA_Handler(
    symbol="AMZN",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
analysis = handler.get_analysis()

# İndikatörleri al
indicators = {
    'RSI': analysis.indicators['RSI'],
    'MACD': analysis.indicators['MACD.macd'],
    'SMA20': analysis.indicators['SMA20'],
    'Volume': analysis.indicators['volume'],
}

# Bunları modelin input'una ek feature olarak ekleyebiliriz
# (ileri seviye — ilk versiyonda sadece Close fiyatı kullan)
```

---

## 🟢 Aşama 7: Dokümantasyon & Kapanış (Süre: ~1-2 saat)

> **Ne yapacağız:** Projeyi toparla, README yaz, her şeyin çalıştığını doğrula.

### 7.1 — `README.md`

**Olması Gerekenler:**
- Proje amacı (1 paragraf)
- Kurulum (adım adım, venv aktivasyonu dahil)
- Dosya yapısı
- Nasıl çalıştırılır (hangi notebook sırayla)
- Sonuçlar (karşılaştırma tablosu + grafik)
- Çıkarımlar (hangi model daha iyi, neden)

### 7.2 — `.gitignore`

```
.venv/
__pycache__/
*.pyc
data/raw/
data/processed/
outputs/models/*.pth
outputs/figures/
logs/
.DS_Store
```

### 7.3 — Doğrulama

```bash
# Her notebook'u baştan sona çalıştır
jupyter nbconvert --to notebook --execute notebooks/01_*.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/02_*.ipynb --inplace
# ... tüm notebook'lar için
```

---

## ⏱️ Zaman Çizelgesi (Gerçekçi)

| Aşama | Ne Öğreneceksin? | Süre |
|-------|-------------------|------|
| **0** | Ortam kurulumu, TradingView auth | 30 dk |
| **1** | yfinance, Pandas keşif, görselleştirme | 2-3 saat |
| **2** | MinMaxScaler, sliding window, tensorler | 2 saat |
| **3** | PyTorch nn.Module, LSTM/GRU teorisi | 2-3 saat |
| **4** | İlk model eğitimi (LSTM) 🎉 | 2-3 saat |
| **5** | İkinci model (GRU) | 1-2 saat |
| **6** | Karşılaştırma, hiperparametre, TradingView ekleme | 2-3 saat |
| **7** | README, .gitignore, son doğrulama | 1 saat |
| **Toplam** | | **~12-17 saat** |

---

## ⚠️ Sık Yapılan Hatalar ve Çözümleri

| Hata | Belirti | Çözüm |
|------|---------|-------|
| **Overfitting** | Train loss düşer, test loss yüksek | Dropout ekle, epoch azalt, model küçült |
| **Underfitting** | Loss hiç düşmez | Learning rate artır, epoch artır, model büyüt |
| **Vanishing Gradient** | Loss çok yavaş düşer | GRU dene (LSTM'den daha az etkilenir) |
| **Data Leakage** | Test sonuçları çok iyi | Scaling'i train verisine göre yap, test'e sızdırma |
| **Yanlış Pencere** | Model hep aynı değeri tahmin eder | lookback'i kontrol et, çok kısa/küçük olabilir |

---

## 📚 Kaynaklar

1. **yfinance:** https://github.com/ranaroussi/yfinance
2. **PyTorch LSTM/GRU:** https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
3. **TradingView Screener:** https://github.com/shner-elmo/tradingview-screener
4. **TradingView TA:** https://github.com/analyzerrest/python-tradingview-ta
5. **Referans Makale:** Stock Price Prediction with PyTorch (Medium)
6. **MinMaxScaler:** https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html