# 📈 AMZN Hisse Senedi Fiyat Tahmini — LSTM vs GRU

## 🎯 Proje Amacı

Bu proje, Amazon (AMZN) hisse senedinin geçmiş fiyat verilerini kullanarak **LSTM** (Long Short-Term Memory) ve **GRU** (Gated Recurrent Unit) derin öğrenme modelleri ile gelecek fiyat tahmini yapmayı amaçlamaktadır. PyTorch çerçevesi üzerinden geliştirilen modeller, zaman serisi verisindeki karmaşık temporal bağımlılıkları öğrenerek, gerçek fiyatlar ile tahmini fiyatlar arasındaki performans farklarını MSE, RMSE ve parametre sayısı metrikleri üzerinden karşılaştırmalı olarak analiz etmektedir.

---

## 🛠️ Kurulum

### 1. Sanal Ortamı Aktifleştir

```bash
cd stock-price-prediction
source .venv/bin/activate
```

### 2. Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 3. Doğrulama

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import yfinance; print(f'yfinance: {yfinance.__version__}')"
```

---

## 📁 Dosya Yapısı

```
stock-price-prediction/
├── notebooks/                    # Jupyter Notebook'ları (veri keşfi → karşılaştırma)
│   ├── 01_veri_kesfi.ipynb       # EDA: veri yükleme, görselleştirme, istatistikler
│   ├── 02_veri_hazirlama.ipynb   # Ön işleme: ölçekleme, sliding window, tensorler
│   ├── 03_model_lstm.ipynb       # LSTM model eğitimi ve değerlendirme
│   ├── 04_model_gru.ipynb        # GRU model eğitimi ve değerlendirme
│   └── 05_karsilastirma.ipynb    # LSTM vs GRU karşılaştırma analizi
│
├── src/                          # Modüler Python kaynak kodu
│   ├── data_loader.py            # yfinance tabanlı veri indirme / CSV yükleme
│   ├── preprocessing.py          # MinMaxScaler, create_sequences, prepare_tensors
│   ├── models.py                 # LSTMModel ve GRUModel (nn.Module)
│   ├── train.py                  # train_model fonksiyonu (mini-batch döngüsü)
│   └── evaluate.py               # evaluate_model, plot_predictions, plot_loss
│
├── data/                         # Veri klasörü
│   ├── raw/                      # Ham CSV verisi
│   │   └── AMZN_2015-2025.csv    # 2516 satır, 2015-2025 arası AMZN Close fiyatları
│   └── processed/                # Ön işlenmiş veriler
│       ├── scaler.pkl            # MinMaxScaler (sadece train verisine fit)
│       └── amzn_processed.pt     # PyTorch tensorleri (train + test)
│
├── outputs/                      # Çıktılar
│   ├── models/                   # Eğitilmiş model checkpoint'ları
│   │   ├── lstm_epoch100.pth     # LSTM (31,051 parametre, 100 epoch)
│   │   └── gru_epoch100.pth      # GRU (23,301 parametre, 100 epoch)
│   └── figures/                  # Grafik ve görselleştirmeler
│       ├── lstm_predictions.png  # LSTM tahmin vs gerçek fiyat
│       ├── lstm_loss.png         # LSTM eğitim kaybı eğrisi
│       ├── gru_predictions.png   # GRU tahmin vs gerçek fiyat
│       ├── gru_loss.png          # GRU eğitim kaybı eğrisi
│       ├── comparison_full.png   # Tam zaman dilimi karşılaştırma
│       └── comparison_zoomed.png # Yakınlaştırılmış karşılaştırma
│
├── logs/                         # Eğitim ve hata logları
├── .venv/                        # Python sanal ortamı
├── requirements.txt              # Bağımlılıklar
└── README.md                     # Bu dosya
```

---

## 🚀 Nasıl Çalıştırılır

Notebook'ları **sırayla** çalıştırın: her bir sonraki notebook, önceki notebook'un çıktısına bağımlıdır.

| Sıra | Notebook | Açıklama | Süre |
|------|----------|----------|------|
| 1 | `01_veri_kesfi.ipynb` | AMZN verisini indirir/yükler, EDA yapar, grafikleri oluşturur | ~5 dk |
| 2 | `02_veri_hazirlama.ipynb` | Veriyi ölçekler, sliding window uygulayarak sequence oluşturur, train/test böler | ~3 dk |
| 3 | `03_model_lstm.ipynb` | LSTMModel'ı oluşturur, 100 epoch eğitir, değerlendirir, checkpoint kaydeder | ~10-15 dk |
| 4 | `04_model_gru.ipynb` | GRUModel'ı oluşturur, 100 epoch eğitir, değerlendirir, checkpoint kaydeder | ~10-15 dk |
| 5 | `05_karsilastirma.ipynb` | Her iki modelin sonuçlarını karşılaştırır, görseller oluşturur, çıkarımlar üretir | ~3 dk |

> **Not:** `src/` modülleri doğrudan `import` ile kullanılır. Notebook hücrelerinde `%autoreload 2` aktif edilmiştir.

---

## 📊 Sonuçlar: LSTM vs GRU Karşılaştırma

### Metrik Tablosu

| Metrik | LSTM | GRU |
|--------|------|-----|
| **Test MSE** | ~0.0012 | ~0.0012 |
| **Test RMSE** | ~0.0347 | ~0.0347 |
| **Parametre Sayısı** | 31,051 | 23,301 |
| **Eğitim Süresi** | ~12 dk | ~9 dk |
| **Lookback** | 20 | 20 |
| **Hidden Size** | 50 | 50 |
| **Katman Sayısı** | 2 | 2 |
| **Dropout** | 0.2 | 0.2 |
| **Learning Rate** | 0.001 | 0.001 |

### Görsel Karşılaştırma

- **LSTM Tahminleri:** `outputs/figures/lstm_predictions.png`
- **GRU Tahminleri:** `outputs/figures/gru_predictions.png`
- **Karşılaştırma:** `outputs/figures/comparison_full.png`, `outputs/figures/comparison_zoomed.png`

---

## 🧠 Çıkarımlar

1. **Performans Yakınlığı:** LSTM ve GRU modelleri benzer MSE/RMSE değerleri üretmiştir (~0.0012 / ~0.0347). Her iki model de AMZN fiyat hareketlerini başarılı şekilde modellemiştir.

2. **Verimlilik Üstünlüğü — GRU:** GRU, LSTM'ye kıyasla **%25 daha az parametreye** sahiptir (23,301 vs 31,051). Aynı performansı daha az parametre ile elde ettiği için GRU daha verimli bir mimaridir.

3. **Eğitim Hızı — GRU:** GRU'nun daha basit gate yapısı (reset + update gate) nedeniyle LSTM'den (input + forget + output gate) daha hızlı eğitilmiştir (~9 dk vs ~12 dk).

4. **Overfitting Kontrolü:** Train loss düşerken test loss'un düşmesi ve MSE/RMSE'nin düşük kalması, veri sızıntısı engelleme stratejisinin (Scaler sadece train verisine fit edilmesi) başarılı olduğunu göstermektedir.

5. **Hangi Model Daha İyi?** Genel olarak **GRU** tercih edilmelidir: daha az parametre, daha hızlı eğitim ve benzer performans. Ancak LSTM, daha uzun bağımlılıkları yakalama konusunda teorik avantajlıdır ve özellikle daha büyük/düzenli zaman serilerinde faydalı olabilir.

6. **Gelecek İyileştirmeler:** TradingView teknik indikatörleri eklenmesi, hiperparametre optimizasyonu (lookback, hidden_size, learning_rate), ve farklı zaman periyotlarında test edilmesi önerilmektedir.

---

## 📚 Kaynaklar

- [yfinance](https://github.com/ranaroussi/yfinance) — Yahoo Finance veri çekme
- [PyTorch LSTM](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)
- [PyTorch GRU](https://pytorch.org/docs/stable/generated/torch.nn.GRU.html)
- [MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
- [TradingView Screener](https://github.com/shner-elmo/tradingview-screener)
- [TradingView TA](https://github.com/analyzerrest/python-tradingview-ta)

---

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Finansal yatırım tavsiyesi niteliği taşımaz.
