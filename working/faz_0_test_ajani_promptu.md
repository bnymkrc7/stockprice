# 🧪 TEST AJANI: FAZ_0 — Ortam Hazırlığı (Süre: ~30 dk)

## 🎯 TEST VE DOĞRULAMA DETAYLARI (PLANDAN OKUNAN)
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

## 📋 TEST UYGULAMA TALİMATLARI
1. Kodlama aşamasında yazılan/değiştirilen tüm dosyaların yerlerin olduğunu doğrulayın.
2. İlgili test senaryolarını çalıştırın (örneğin import testleri, model ileri besleme testleri veya veri doğrulama testleri).
3. Test çıktılarında herhangi bir `WARNING` veya `HATA` olmadığından emin olun (oturum bulunamadığında graceful fallback kullanın).
4. Test sonuçlarını `working/test_report_faz_0.md` dosyası olarak kaydedin.
5. Başarılı sonuçları Orkestratör Ajanına rapor edin.
