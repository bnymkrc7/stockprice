# Faz 4: LSTM Model Eğitimi — ✅ Tamamlandı

## Yapılan İşler

### 1. Notebook Oluşturuldu: `notebooks/03_model_lstm.ipynb`
- 6 hücreli Jupyter notebook hazırlanmıştır.
- Hücreler: Setup → Veri Yükleme → Model Oluşturma → Eğitim → Değerlendirme → Kaydetme

### 2. Hücre Detayları

| # | İçerik | Açıklama |
|---|--------|----------|
| 1 | Setup | `autoreload`, `torch`, `src.models`, `src.train`, `src.evaluate` importları; CUDA/CPU cihaz seçimi |
| 2 | Veri Yükleme | `amzn_processed.pt` ve `scaler.pkl` dosyaları `data/processed/` dizininden yüklenir |
| 3 | Model Oluşturma | `LSTMModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)` — parametre sayısı gösterilir |
| 4 | Eğitim | `train_model()` fonksiyonu 100 epoch, lr=0.001, device='cuda/cpu' parametreleriyle çalıştırılır |
| 5 | Değerlendirme | `evaluate_model()` ile MSE/RMSE hesaplanır; `plot_predictions()` ve `plot_loss()` grafikleri `outputs/figures/` dizinine kaydedilir |
| 6 | Kaydetme | Model state dict + hiperparametreler + metrikler `outputs/models/lstm_epoch100.pth` dosyasına kaydedilir |

### 3. Veri Sızıntısı Kontrolü
- Veriler Faz 2'de train/test split yapıldıktan sonra kaydedildi.
- Scaler sadece training verisine fit edildi (Faz 2 doğrulandı).
- Notebook, Faz 2'den hazırlanmış güvenli veriyi doğrudan kullanır — sızıntı riski yoktur.

### 4. Modülerlik
- Model: `src/models.py` (LSTMModel)
- Eğitim: `src/train.py` (train_model)
- Değerlendirme: `src/evaluate.py` (evaluate_model, plot_predictions, plot_loss)
- Notebook sadece orchestrator katmanı — tüm mantık modüllerde.

### 5. task.md Güncellendi
- Faz 4 durumu `[/]` (devam ediyor) → `[x]` (tamamlandı) olarak güncellendi.

## Dosyalar
- ✅ `notebooks/03_model_lstm.ipynb` — Notebook
- ✅ `task.md` — Faz 4 tamamlandı olarak işaretlendi
- ✅ `working/done_faz_4.md` — Bu özet dosya
