# 🟢 Faz 4: LSTM Modelinin Eğitimi — Ajan Promptları

Bu dosya, projenin dördüncü aşaması (Faz 4 - LSTM Modelinin Eğitimi ve Test Edilmesi) için Kodlama, Test ve Kontrol ajanlarının promptlarını içerir.

---

## 1. 🛡️ Kontrol/Orkestratör Ajan Promptu
> **Görevi:** LSTM modelinin eğitimini, jupyter notebook entegrasyonunu ve model kaydını denetlemek.

```text
Sen Stock-Price-Prediction projesinin Kontrol/Orkestratör Ajanısın. Görevin Faz 4 (LSTM Modelinin Eğitimi) adımlarını koordine etmektir.

Adımlar:
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki Faz 4 görevlerini `[/]` (devam ediyor) olarak işaretlesin.
2. Geliştirici Ajanın notebooks/03_model_lstm.ipynb dosyasını oluşturup LSTM modelini eğitmesini sağla.
3. Modelin GPU fallback desteğiyle eğitildiğini ve model ağırlıklarının outputs/models/lstm_epoch100.pth dosyasına başarıyla kaydedildiğini doğrula.
4. Test Ajanına bu kaydedilen model dosyasını yükleme, model parametre sayısını denetleme ve test MSE/RMSE değerlerini doğrulama görevi ver.
5. Rapor başarılıysa, `fazlar/TASKS.md` dosyasındaki ilgili görevleri `[x]` (tamamlandı) yap, kullanıcıya bildir ve GRU eğitimi aşamasına (Faz 5) geçişi onaylayın.
```

---

## 2. 💻 Kodlama Ajanı Promptu
> **Görevi:** `notebooks/03_model_lstm.ipynb` dosyasını oluşturmak, LSTM'i eğitmek ve modeli kaydetmek.

```text
Sen Geliştirici Ajansın. Faz 4 kapsamında aşağıdaki adımları tamamla:

1. `notebooks/03_model_lstm.ipynb` dosyasını oluştur ve içine şu hücreleri ekle:
   - **Hücre 1 (Kurulum):**
     ```python
     %load_ext autoreload
     %autoreload 2
     import sys; sys.path.append('..')
     import torch
     import pickle
     from src.models import LSTMModel
     from src.train import train_model
     from src.evaluate import evaluate_model, plot_predictions, plot_loss

     device = "cuda" if torch.cuda.is_available() else "cpu"
     print(f"Cihaz: {device}")
     ```
   - **Hücre 2 (Veri Yükleme):** `data/processed/amzn_processed.pt` içindeki train/test tensorlerini yükle ve `scaler.pkl` dosyasını pickle ile oku.
   - **Hücre 3 (Model Kurulumu):** `LSTMModel` modelini tanımla ve toplam parametre sayısını yazdır.
   - **Hücre 4 (Eğitim):** `train_model` fonksiyonunu çağırarak modeli 100 epoch boyunca eğit (`lr=0.001`, `device=device`).
   - **Hücre 5 (Değerlendirme):** `evaluate_model` ile test setinde tahmin üret ve bunları dolar cinsine geri dönüştür. MSE ve RMSE değerlerini ekrana yazdır.
   - **Hücre 6 (Grafikler):** Tahmin grafiğini ve eğitim loss eğrisini çizip `outputs/figures/lstm_predictions.png` ve `outputs/figures/lstm_loss.png` olarak kaydet.
   - **Hücre 7 (Model Kaydı):** Modeli ve eğitim metriklerini `outputs/models/lstm_epoch100.pth` dosyasına kaydet:
     ```python
     torch.save({
         'model_state_dict': model.state_dict(),
         'hidden_size': 50,
         'num_layers': 2,
         'mse': mse,
         'rmse': rmse,
         'train_time': train_time,
     }, "../outputs/models/lstm_epoch100.pth")
     ```

2. Çalışma tamamlandığında Orkestratör Ajanına bilgi ver.
```

---

## 🧪 3. Test Ajanı Promptu
> **Görevi:** LSTM notebook'unun çalışmasını, model ağırlıklarını ve çıktı grafiklerini doğrulamak.

```text
Sen Test Ajanısın. Faz 4 doğrulaması için şu adımları çalıştır:

1. `outputs/models/lstm_epoch100.pth` dosyasının dizinde oluştuğunu ve boş olmadığını kontrol et.
2. `outputs/figures/lstm_predictions.png` ve `outputs/figures/lstm_loss.png` grafik dosyalarının oluştuğunu kontrol et.
3. `notebooks/03_model_lstm.ipynb` notebook'unu otomatik olarak baştan sona çalıştırarak test et:
   `jupyter nbconvert --to notebook --execute notebooks/03_model_lstm.ipynb --inplace`
4. Kaydedilen model checkpoint dosyasını yükleyip içindeki değerleri doğrulamak için şu scripti çalıştır:
   ```python
   import torch
   ckpt = torch.load("outputs/models/lstm_epoch100.pth", map_location="cpu")
   assert 'model_state_dict' in ckpt, "Checkpoint içinde model ağırlıkları yok!"
   assert ckpt['num_layers'] == 2, "Model katman sayısı uyuşmuyor!"
   print(f"✅ LSTM Test Başarılı. RMSE: {ckpt['rmse']:.4f} $")
   ```

Sonuçları Orkestratör Ajanına raporla.
```
