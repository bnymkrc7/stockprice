# ✅ Faz 3 — Model Mimarileri: Tamamlandı

## Yapılan İşler

### 1. `src/models.py` — LSTM ve GRU Model Sınıfları
- **LSTMModel**: 2 katmanlı LSTM (`hidden=50, num_layers=2, dropout=0.2`), batch_first=True, son adımdan linear katman çıkışı
- **GRUModel**: LSTM ile aynı parametrelerde GRU (daha hızlı, LSTM'e yakın performans)
- `batch_first=True`: girdiyi (batch, seq, features) formatında alır
- `out[:, -1, :]`: son adımdaki hidden state'den tahmin yapılır

### 2. `src/train.py` — Eğitim Döngüsü
- **train_model()**: Standart PyTorch eğitim döngüsü
- Mini-batch eğitim (DataLoader + shuffle)
- Adam optimizer (lr=0.001), MSE Loss
- Opsiyonel validation verisi desteği (overfitting tespiti)
- Epoch başına ortalama loss, toplam süre, son loss çıktısı
- `optimizer.zero_grad()` ile gradyan birikimini önler

### 3. `src/evaluate.py` — Değerlendirme ve Görselleştirme
- **evaluate_model()**: Test setinde MSE ve RMSE metrikleri
  - Scaler desteği: tahminleri orijinal fiyata geri çevirir
  - `torch.no_grad()` ile bellek tasarrufu
- **plot_predictions()**: Gerçek vs tahmin karşılaştırmalı çizim
- **plot_loss()**: Eğitim loss eğrisi çizimi

### 4. `task.md` Güncellendi
- Faz 3 durumu `[/]` (devam ediyor) olarak işaretlendi

### 5. `working/done_faz_3.md` Oluşturuldu (bu dosya)

## Kod Kalitesi
- ✅ Veri sızıntısı önleme: Sadece training verisi üzerinde fit edilen scaler kullanımı korundu
- ✅ Modülerlik: Her fonksiyon/sınıf ayrı dosyada, bağımlılıklar minimum
- ✅ Temiz kod: Tip ipuçları (type hints), docstring'ler, anlamlı değişken isimleri
- ✅ Lint temiz: Pyright syntax kontrolü geçiyor
