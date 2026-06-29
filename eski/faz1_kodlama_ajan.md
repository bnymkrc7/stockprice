# Faz 1: Veri Toplama & Keşif
# Kodlama Ajanı Promptu

## GÖREV
Proje: `/home/zorildiz/projeler/bunyamin/stock-price-prediction`
Faz 1: yfinance ile hisse verisi çekme, veri keşfi ve görselleştirme

## BAĞLAM
- Faz 0 tamamlandı: Ortam hazır, paketler kurulu
- Hedef: AMZN (Amazon) hissesinin 2015-2025 arası günlük verisini çekmek
- Çıktı: `src/data_loader.py` modülü + `notebooks/01_veri_kesfi.ipynb`

## YAPILACAKLAR

### 1. `src/data_loader.py` Oluşturma

```python
# src/data_loader.py
"""
Hisse senedi verisi indirme ve yükleme modülü.
yfinance kullanarak tarihsel OHLCV verisi çeker.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
from typing import Optional

def fetch_stock_data(
    ticker: str = "AMZN",
    start: str = "2015-01-01",
    end: str = "2025-01-01",
    save_path: Optional[str] = None
) -> pd.DataFrame:
    """
    yfinance ile hisse senedi verisi indirir.
    
    Parametreler:
        ticker: Hisse sembolü (örn: AMZN, AAPL, GOOGL)
        start: Başlangıç tarihi (YYYY-MM-DD formatı)
        end: Bitiş tarihi (YYYY-MM-DD formatı)
        save_path: CSV'ye kaydetmek için yol (opsiyonel)
    
    Döner:
        pd.DataFrame: OHLCV verisi (Open, High, Low, Close, Volume)
    
    Not:
        - yfinance ücretsiz, API key gerekmez
        - Veri Yahoo Finance'dan çekilir
        - MultiIndex sütunlar düzleştirilir
    """
    print(f"📥 {ticker} verisi indiriliyor ({start} - {end})...")
    
    # Veriyi indir
    df = yf.download(ticker, start=start, end=end, progress=True)
    
    # MultiIndex sütunları düzleştir (eğer varsa)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Tarih index'ini ayarla
    df.index = pd.to_datetime(df.index)
    
    print(f"✅ {len(df)} satır veri indirildi")
    print(f"   Tarih aralığı: {df.index[0]} → {df.index[-1]}")
    print(f"   Sütunlar: {list(df.columns)}")
    
    # Kaydet (eğer path verilmişse)
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path)
        print(f"💾 Kaydedildi: {save_path}")
    
    return df

def load_local_data(path: str) -> pd.DataFrame:
    """
    Daha önce kaydedilmiş CSV'yi yükler.
    
    Parametreler:
        path: CSV dosya yolu
    
    Döner:
        pd.DataFrame: Yüklenen veri
    """
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    print(f"📂 Yerel dosyadan yüklendi: {path}")
    print(f"   {len(df)} satır veri")
    return df
```

### 2. `notebooks/01_veri_kesfi.ipynb` Oluşturma

Jupyter notebook'u şu hücrelerle oluştur:

**Hücre 1: Setup**
```python
%load_ext autoreload
%autoreload 2
import sys
sys.path.append('..')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import fetch_stock_data, load_local_data

sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 6)
```

**Hücre 2: Veri İndirme/Yükleme**
```python
# Veriyi indir (veya yerel dosyadan yükle)
df = fetch_stock_data(
    ticker="AMZN",
    start="2015-01-01",
    end="2025-01-01",
    save_path="../data/raw/AMZN_2015-2025.csv"
)
```

**Hücre 3: Veri Keşfi - Temel İnceleme**
```python
print("📊 Veri Bilgisi:")
print("=" * 50)
df.info()
print("\n📈 İlk 5 Satır:")
print(df.head())
print("\n📉 Son 5 Satır:")
print(df.tail())
```

**Hücre 4: İstatistiksel Özet**
```python
print("📊 İstatistiksel Özet:")
print("=" * 50)
print(df.describe())
```

**Hücre 5: Eksik Veri Kontrolü**
```python
print("❓ Eksik Veri Kontrolü:")
print("=" * 50)
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "Eksik veri yok.")
```

**Hücre 6: Kapanış Fiyatı Grafiği**
```python
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['Close'], label='Kapanış Fiyatı', linewidth=1.5)
plt.plot(df.index, df['Close'].rolling(20).mean(), label='20 Günlük SMA', alpha=0.7, linestyle='--')
plt.plot(df.index, df['Close'].rolling(50).mean(), label='50 Günlük SMA', alpha=0.7, linestyle='--')
plt.title('Amazon (AMZN) Hisse Fiyatı - Kapanış')
plt.xlabel('Tarih')
plt.ylabel('Fiyat ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('../outputs/figures/amzn_close_price.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Hücre 7: Günlük Getiri Analizi**
```python
df['Daily_Return'] = df['Close'].pct_change()

plt.figure(figsize=(14, 4))
df['Daily_Return'].hist(bins=50, alpha=0.7, edgecolor='black')
plt.title('AMZN Günlük Getiri Dağılımı')
plt.xlabel('Getiri (%)')
plt.ylabel('Frekans')
plt.axvline(x=0, color='red', linestyle='--', linewidth=2)
plt.savefig('../outputs/figures/amzn_daily_returns.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"📊 Günlük Getiri İstatistikleri:")
print(f"   Ortalama: {df['Daily_Return'].mean():.4f} ({df['Daily_Return'].mean()*100:.2f}%)")
print(f"   Std Sapma: {df['Daily_Return'].std():.4f}")
print(f"   Min: {df['Daily_Return'].min():.4f}")
print(f"   Max: {df['Daily_Return'].max():.4f}")
```

**Hücre 8: Hacim Analizi**
```python
plt.figure(figsize=(14, 3))
plt.bar(df.index, df['Volume'], alpha=0.5)
plt.title('AMZN İşlem Hacmi')
plt.xlabel('Tarih')
plt.ylabel('Hacim')
plt.savefig('../outputs/figures/amzn_volume.png', dpi=150, bbox_inches='tight')
plt.show()
```

## ÇIKTI BEKLENTİLERİ
1. ✅ `src/data_loader.py` - Veri indirme/yükleme fonksiyonları
2. ✅ `data/raw/AMZN_2015-2025.csv` - Ham veri dosyası
3. ✅ `notebooks/01_veri_kesfi.ipynb` - Keşif notebook'u
4. ✅ `outputs/figures/amzn_close_price.png` - Kapanış fiyat grafiği
5. ✅ `outputs/figures/amzn_daily_returns.png` - Getiri dağılım grafiği
6. ✅ `outputs/figures/amzn_volume.png` - Hacim grafiği

## KISITLAMALAR
- Sadece AMZN verisi kullanılacak (başka hisse opsiyonel)
- Tarih aralığı: 2015-01-01 ile 2025-01-01
- Veri günlük (daily) interval'de olacak
- Eksik veriler varsa `dropna()` veya `fillna()` ile处理

## NOTLAR
- yfinance bazen hata verebilir, retry mekanizması ekle (max 3 deneme)
- Veri büyükse (10 yıl) bellekte tutmak sorun olmaz (~2500 satır)
- Grafikler yüksek çözünürlükte (dpi=150) kaydedilecek