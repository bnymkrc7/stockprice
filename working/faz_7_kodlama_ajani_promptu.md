# 💻 GELİŞTİRİCİ GÖREVİ: FAZ_7 — Dokümantasyon & Kapanış (Süre: ~1-2 saat)

## 🎯 GÖREV DETAYLARI (PLANDAN OKUNAN)
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

## 🔄 GELİŞTİRİCİ İŞ AKIŞI
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki FAZ_7 görevini `[/]` (devam ediyor) olarak işaretlesin.
2. Yukarıda belirtilen kodlama hedeflerini, modülerlik ve veri sızıntısını önleme kurallarına uyarak kodlayın.
3. Çalışma bittiğinde `working/done_faz_7.md` adında bir done dosyası oluşturarak yapılan işleri özetleyin.
4. Değişikliklerinizi test ajanı ile doğrulamaya hazır hale getirin.
