# 🟢 Faz 3: Model Mimarileri ve Eğitim Altyapısı — Ajan Promptları

Bu dosya, projenin üçüncü aşaması (Faz 3 - Model Mimarileri ve Modüller) için Kodlama, Test ve Kontrol ajanlarının promptlarını içerir.

---

## 1. 🛡️ Kontrol/Orkestratör Ajan Promptu
> **Görevi:** Modüler PyTorch altyapısının (modeller, eğitim fonksiyonu, değerlendirme metrikleri) kurulmasını koordine etmek.

```text
Sen Stock-Price-Prediction projesinin Kontrol/Orkestratör Ajanısın. Görevin Faz 3 (Model Mimarileri ve Eğitim Altyapısı) adımlarının doğru şekilde kurulmasını koordine etmektir.

Adımlar:
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki Faz 3 görevlerini `[/]` (devam ediyor) olarak işaretlesin.
2. Geliştirici Ajanın src/ dizini altına models.py, train.py ve evaluate.py dosyalarını yazmasını sağla.
3. Yazılan modüllerin PyTorch standartlarına ve modüler programlama ilkelerine uygunluğunu kontrol et.
4. Test Ajanına bu modüllerin import testlerini ve basit bir sahte (dummy) veriyle ileri besleme/geri yayılım (forward/backward) yapabildiğini doğrulama görevi ver.
5. Testler başarılıysa, `fazlar/TASKS.md` dosyasındaki ilgili görevleri `[x]` (tamamlandı) yap, kullanıcıya bildir ve LSTM eğitimi aşamasına (Faz 4) geçişi onaylayın.
```

---

## 2. 💻 Kodlama Ajanı Promptu
> **Görevi:** `src/models.py`, `src/train.py` ve `src/evaluate.py` modüllerini kodlamak.

```text
Sen Geliştirici Ajansın. Faz 3 kapsamında aşağıdaki üç Python modülünü oluştur:

1. `src/models.py`:
   - `LSTMModel` ve `GRUModel` sınıflarını `nn.Module` üzerinden tanımla.
   - Her iki model de 2 katmanlı (num_layers=2), hidden_size=50 ve dropout=0.2 olmalıdır.
   - Batch-first formatını desteklemelidir: `batch_first=True`.
   - Forward pass sonrasında dizinin son elemanının çıktısını linear katmana beslemelidir (`out[:, -1, :]`).
   ```python
   import torch.nn as nn

   class LSTMModel(nn.Module):
       def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
           super().__init__()
           self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
           self.fc = nn.Linear(hidden_size, 1)

       def forward(self, x):
           out, _ = self.lstm(x)
           return self.fc(out[:, -1, :])

   class GRUModel(nn.Module):
       def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
           super().__init__()
           self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
           self.fc = nn.Linear(hidden_size, 1)

       def forward(self, x):
           out, _ = self.gru(x)
           return self.fc(out[:, -1, :])
   ```

2. `src/train.py`:
   - `train_model(model, X_train, y_train, epochs=100, lr=0.001, device="cpu", verbose=True)` fonksiyonunu tanımla.
   - `nn.MSELoss` ve `torch.optim.Adam` kullan.
   - Her adımda gradyanları sıfırla (`optimizer.zero_grad()`), geri yayılım yap (`loss.backward()`) ve ağırlıkları güncelle (`optimizer.step()`).
   - Eğitim süresini ölç ve `loss_history` ile birlikte eğitim süresini geri döndür.

3. `src/evaluate.py`:
   - `evaluate_model(model, X_test, y_test, scaler=None, device="cpu")` fonksiyonunu tanımla.
   - Model değerlendirme sırasında gradyan hesaplamayı devre dışı bırak (`with torch.no_grad():`).
   - Tahminleri ve gerçek değerleri `scaler.inverse_transform` kullanarak orijinal fiyatlarına geri dönüştür.
   - MSE ve RMSE metriklerini hesaplayıp döndür.
   - Grafik çizimleri için `plot_predictions(actuals, preds, title, save_path)` ve `plot_loss(loss_history, title, save_path)` yardımcı fonksiyonlarını ekle.

Kodlama bittiğinde Orkestratör Ajanına bildir.
```

---

## 🧪 3. Test Ajanı Promptu
> **Görevi:** Modüllerin import durumunu, model yapısını ve sahte veriyle ileri/geri besleme testlerini doğrulamak.

```text
Sen Test Ajanısın. Faz 3 doğrulaması için şu adımları çalıştır:

1. `src/models.py`, `src/train.py` ve `src/evaluate.py` dosyalarının belirtilen yollarda oluştuğunu doğrula.
2. Yazılan modüllerin import edilebildiğini ve sahte bir veri üzerinde hatasız çalıştığını doğrulamak için şu test scriptini çalıştır:
   ```python
   import torch
   from src.models import LSTMModel, GRUModel
   from src.train import train_model
   
   # Sahte veri oluştur (10 örnek, 20 zaman adımı, 1 feature)
   X_dummy = torch.randn(10, 20, 1)
   y_dummy = torch.randn(10, 1)
   
   # Modelleri oluştur
   lstm = LSTMModel()
   gru = GRUModel()
   
   # İleri besleme testi
   out_lstm = lstm(X_dummy)
   out_gru = gru(X_dummy)
   assert out_lstm.shape == (10, 1), "LSTM çıktı boyutu yanlış!"
   assert out_gru.shape == (10, 1), "GRU çıktı boyutu yanlış!"
   print("✅ İleri besleme testi başarılı.")
   
   # Hızlı eğitim testi (5 epoch)
   loss_hist, elapsed = train_model(lstm, X_dummy, y_dummy, epochs=5, verbose=False)
   assert len(loss_hist) == 5, "Eğitim epoch sayısı uyuşmuyor!"
   print(f"✅ Eğitim altyapısı testi başarılı. Süre: {elapsed:.4f} sn")
   ```

Sonuçları Orkestratör Ajanına raporla.
```
