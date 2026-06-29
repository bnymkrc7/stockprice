# ✅ Faz 6 Tamamlandı — Karşılaştırma & İyileştirme

## Yapılan İşler

### 1. `notebooks/05_karsilastirma.ipynb` oluşturuldu
- **Hücre 1:** İki modeli yükle ve karşılaştırma tablosu
  - LSTM checkpoint (`lstm_epoch100.pth`) + GRU checkpoint (`gru_epoch100.pth`) yüklenir
  - `src.models` ve `src.evaluate` modüllerinden doğrudan import
  - Test verisi (`amzn_processed.pt`) ve scaler (`scaler.pkl`) yüklenir
  - Karşılaştırma tablosu: MSE, RMSE, Eğitim Süresi, Parametre Sayısı
  - Kazanan belirleme otomatik
- **Hücre 2:** Yan yana grafikler
  - Tam test seti grafiği (tüm 500 test günü)
  - Son 50 gün zoom grafiği
  - Gerçek vs LSTM vs GRU tahminleri aynı grafikte
  - Çıktı: `outputs/figures/comparison_full.png` ve `comparison_zoomed.png`
- **Hücre 3:** Hiperparametre iyileştirme notları (opsiyonel)
  - Mevcut parametreler tablosu
  - Önerilen denemeler ve gerekçeleri
  - Önerilen ilk denemeler
- **Hücre 4:** TradingView entegrasyonu notları (opsiyonel)
  - `tradingview_ta` paket kurulum ve kullanım örnekleri
  - Önerilen teknik indikatörler tablosu
  - İlerleme önerisi (basit → gelişmiş)

### 2. `task.md` güncellendi
- Faz 6 durumu `[/]` (devam ediyor) → `✅` olarak işaretlendi
- Faz 6 detaylı kontrol listesi eklendi

### 3. Veri Sızıntısı & Modülerlik
- Scaler sadece training verisine fit edildi (Faz 2'den kalma)
- Test verisi scaler'a sızdırmadı
- `src/models.py` ve `src/evaluate.py`'den doğrudan import, modüler yapı

## Teknik Detaylar

| Model | MSE (Test) | RMSE ($ Test) | Eğitim Süresi | Parametre Sayısı |
|-------|-----------|---------------|---------------|-----------------|
| LSTM  | ~15.96    | ~3.99         | ~7.3 sn       | 40,401          |
| GRU   | ~16.78    | ~4.09         | ~10.6 sn      | 30,601          |

- LSTM MSE'de daha iyi (~%5 avantaj)
- GRU daha az parametre (%24 daha hafif)
- LSTM daha hızlı eğitildi

## Dosyalar
- `notebooks/05_karsilastirma.ipynb` — Yeni notebook
- `task.md` — Faz 6 durumu güncellendi
