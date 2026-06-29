# Faz 0: Ortam Hazırlığı & Kurulum
# Test Ajanı Promptu

## GÖREV
Proje: `/home/zorildiz/projeler/bunyamin/stock-price-prediction`
Faz 0 Testi: Ortam kurulumunun doğrulanması ve tüm bağımlılıkların çalıştığının teyidi

## TEST SENARYOLARI

### 1. Sanal Ortam Doğrulama
```bash
# .venv'in varlığını ve aktifliğini kontrol et
ls -la .venv/bin/python
.venv/bin/python --version
```

### 2. Paket Kurulumu ve Versiyon Kontrolü
```bash
# Tüm gerekli paketleri kontrol et
.venv/bin/pip list | grep -E "torch|pandas|numpy|yfinance|seaborn|tradingview|rookiepy"
```

### 3. Temel Import Testleri
```python
# test_imports.py
import torch
import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import tradingview_screener
import tradingview_ta
import rookiepy

print("✅ Tüm paketler başarıyla import edildi.")
```

### 4. CUDA/GPU Doğrulama
```python
# test_cuda.py
import torch

if torch.cuda.is_available():
    print(f"✅ CUDA mevcut: {torch.cuda.get_device_name(0)}")
    print(f"   GPU bellek: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️ CUDA mevcut değil. CPU modunda çalışılacak.")
```

### 5. Veri Çekme Testi (yfinance)
```python
# test_yfinance.py
import yfinance as yf
import pandas as pd

def test_yfinance_download():
    """Basit veri çekme testi"""
    try:
        df = yf.download("AMZN", start="2020-01-01", end="2020-01-10", progress=False)
        assert len(df) > 0, "Veri boş döndü"
        assert "Close" in df.columns, "Close sütunu eksik"
        print(f"✅ yfinance testi başarılı: {len(df)} satır veri")
        return True
    except Exception as e:
        print(f"❌ yfinance testi başarısız: {e}")
        return False

if __name__ == "__main__":
    test_yfinance_download()
```

### 6. Klasör Yapısı Kontrolü
```bash
# test_directory_structure.sh
#!/bin/bash
echo "📁 Klasör yapısı kontrolü..."
required_dirs=("data/raw" "data/processed" "outputs/figures" "outputs/models")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir mevcut"
    else
        echo "❌ $dir eksik!"
        exit 1
    fi
done
echo "✅ Tüm klasörler mevcut."
```

### 7. requirements.txt Doğrulama
```bash
# test_requirements.sh
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt mevcut"
    echo "📦 İçerik:"
    cat requirements.txt
else
    echo "❌ requirements.txt eksik!"
    exit 1
fi
```

### 8. TradingView Cookie Testi (Opsiyonel)
```python
# test_tradingview.py
try:
    import rookiepy
    from tradingview_screener import Query
    
    # Chrome'dan cookie al (sadece çalıştırılabilirse)
    cookies = rookiepy.to_cookiejar(rookiepy.chrome(['.tradingview.com']))
    total, df = Query().get_scanner_data(cookies=cookies)
    print(f"✅ TradingView testi başarılı: {total} kayıt")
except ImportError:
    print("⚠️ rookiepy yüklü değil, atlanıyor")
except Exception as e:
    print(f"⚠️ TradingView testi başarısız (opsiyonel): {e}")
```

## BEKLENEN SONUÇLAR

| Test | Beklenen Sonuç |
|------|----------------|
| Sanal ortam | ✅ .venv aktif, Python 3.12+ |
| PyTorch | ✅ PyTorch 2.12+, CUDA durumunu bildir |
| Paketler | ✅ yfinance, seaborn, tradingview-screener, tradingview-ta, rookiepy kurulu |
| Import testleri | ✅ Tüm paketler sorunsuz import edilebilir |
| CUDA/GPU | ✅ GPU varsa isim ve bellek bilgisi, yoksa CPU uyarısı |
| yfinance | ✅ AMZN verisi başarıyla çekilebilir |
| Klasör yapısı | ✅ data/raw, data/processed, outputs/figures, outputs/models mevcut |
| requirements.txt | ✅ Dosya mevcut ve tüm paketler listelenmiş |
| TradingView | ⚠️ Opsiyonel, başarısız olursa uyarı ver |

## ÇIKTI FORMATI

Testler tamamlandığında şu formatta özet rapor oluştur:

```
==================================================
FAZ 0 TEST SONUCU
==================================================
✅ Ortam Doğrulama: PASSED
✅ Paket Kurulumu: PASSED
✅ Import Testleri: PASSED
✅ CUDA Kontrolü: {GPU VAR/YOK}
✅ Veri Çekme Testi: PASSED
✅ Klasör Yapısı: PASSED
✅ requirements.txt: PASSED
⚠️ TradingView: SKIPPED/FAILED (opsiyonel)

📊 TOPLAM: 8/9 TEST BAŞARILI
==================================================
```

## BAŞARI KRİTERLERİ
- Tüm zorunlu testler (1-7) başarılı olmalı
- TradingView testi opsiyonel, başarısız olsa da faz 0 tamam sayılır
- `test_env.py` çalıştırıldığında hata vermemeli
- Sonraki fazlar (veri toplama, ön işleme) için ortam hazır olmalı