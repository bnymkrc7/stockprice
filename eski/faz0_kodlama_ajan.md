# Faz 0: Ortam Hazırlığı & Kurulum
# Kodlama Ajanı Promptu

## GÖREV
Proje: `/home/zorildiz/projeler/bunyamin/stock-price-prediction`
Faz 0: Ortam doğrulama, paket kurulumu, klasör yapısı oluşturma

## BAĞLAM
- Proje zaten `.venv` (Python 3.12 + PyTorch 2.12) içeriyor
- Hedef: Hisse senedi fiyat tahmini için LSTM & GRU modelleri eğitmek
- Veri kaynağı: yfinance (ücretsiz, API key gerekmez)
- Ek özellik: TradingView entegrasyonu (opsiyonel)

## YAPILACAKLAR

### 1. Ortam Doğrulama
```bash
source .venv/bin/activate
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
```

### 2. Paket Kurulumu
```bash
pip install yfinance seaborn tradingview-screener tradingview-ta rookiepy
```

### 3. Klasör Yapısı Oluşturma
```bash
mkdir -p data/raw data/processed outputs/figures outputs/models
```

### 4. requirements.txt Oluşturma
```bash
pip freeze > requirements.txt
```

### 5. TradingView Cookie Setup (Opsiyonel)
- Chrome'dan TradingView cookie'lerini `rookiepy` ile export et
- `test_tradingview.py` scripti oluştur ve cookie ile veri çekmeyi dene

## KODLAMA TALİMATLARI

### Test Script: `test_env.py`
```python
#!/usr/bin/env python3
"""Ortam doğrulama scripti"""
import sys
import torch
import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns

print("=" * 50)
print("🔍 ORTAM DOĞRULAMA")
print("=" * 50)
print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}")
print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
print(f"yfinance: {yf.__version__}")
print(f"seaborn: {sns.__version__}")
print("=" * 50)

# Basit veri çekme testi
print("\n📥 Veri çekme testi (AMZN)...")
try:
    df = yf.download("AMZN", start="2020-01-01", end="2020-01-10", progress=False)
    print(f"✅ Başarılı! {len(df)} satır veri çekildi.")
    print(f"   Sütunlar: {list(df.columns)}")
except Exception as e:
    print(f"❌ Hata: {e}")
    sys.exit(1)
```

## ÇIKTI BEKLENTİLERİ
1. ✅ Ortam doğrulama çıktısı (PyTorch, CUDA, paket versiyonları)
2. ✅ `data/raw/`, `data/processed/`, `outputs/figures/`, `outputs/models/` klasörleri oluşturulmuş
3. ✅ `requirements.txt` oluşturulmuş
4. ✅ `test_env.py` çalıştırılabilir ve başarılı
5. ✅ (Opsiyonel) TradingView cookie test scripti `test_tradingview.py`

## KISITLAMALAR
- `.venv` içinde çalışılacak
- Sadece gerekli paketler kurulacak (yfinance, seaborn, tradingview-screener, tradingview-ta, rookiepy)
- TradingView entegrasyonu opsiyonel, ana odak yfinance

## NOTLAR
- Eğer CUDA yoksa sorun değil, CPU'da da çalışır
- TradingView cookie setup'ı karmaşık olabilir, başarısız olursa sadece yfinance ile devam et