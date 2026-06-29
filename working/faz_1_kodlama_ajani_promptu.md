# 💻 GELİŞTİRİCİ GÖREVİ: FAZ_1 — Veri Toplama ve Keşif (Süre: ~2-3 saat)

## 🎯 GÖREV DETAYLARI (PLANDAN OKUNAN)
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

## 🔄 GELİŞTİRİCİ İŞ AKIŞI
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki FAZ_1 görevini `[/]` (devam ediyor) olarak işaretlesin.
2. Yukarıda belirtilen kodlama hedeflerini, modülerlik ve veri sızıntısını önleme kurallarına uyarak kodlayın.
3. Çalışma bittiğinde `working/done_faz_1.md` adında bir done dosyası oluşturarak yapılan işleri özetleyin.
4. Değişikliklerinizi test ajanı ile doğrulamaya hazır hale getirin.
