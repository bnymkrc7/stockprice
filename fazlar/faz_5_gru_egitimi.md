# 🟢 Faz 5: GRU Modelinin Eğitimi — Ajan Promptları

Bu dosya, projenin beşinci aşaması (Faz 5 - GRU Modelinin Eğitimi ve Test Edilmesi) için Kodlama, Test ve Kontrol ajanlarının promptlarını içerir.

---

## 1. 🛡️ Kontrol/Orkestratör Ajan Promptu
> **Görevi:** GRU modelinin adil (fair comparison) şartlarda eğitilmesini ve model kaydını denetlemek.

```text
Sen Stock-Price-Prediction projesinin Kontrol/Orkestratör Ajanısın. Görevin Faz 5 (GRU Modelinin Eğitimi) adımlarını koordine etmektir.

Adımlar:
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki Faz 5 görevlerini `[/]` (devam ediyor) olarak işaretlesin.
2. Geliştirici Ajanın notebooks/04_model_gru.ipynb dosyasını oluşturup GRU modelini eğitmesini sağla.
3. Modelin LSTM ile birebir aynı veri, lookback ve hiperparametrelerle (hidden_size=50, num_layers=2, epochs=100) eğitildiğini doğrula.
4. Model ağırlıklarının outputs/models/gru_epoch100.pth dosyasına başarıyla kaydedildiğinden emin ol.
5. Test Ajanına bu kaydedilen GRU model dosyasını yükleme ve doğrulama görevi ver.
6. Rapor başarılıysa, `fazlar/TASKS.md` dosyasındaki ilgili görevleri `[x]` (tamamlandı) yap, kullanıcıya bildir ve Karşılaştırma ve Kapanış aşamasına (Faz 6) geçişi onaylayın.
```

---

## 2. 💻 Kodlama Ajanı Promptu
> **Görevi:** `notebooks/04_model_gru.ipynb` dosyasını oluşturmak, GRU'yu eğitmek ve modeli kaydetmek.

```text
Sen Geliştirici Ajansın. Faz 5 kapsamında adil karşılaştırma (fair comparison) şartlarına uyarak aşağıdaki adımları tamamla:

1. `notebooks/04_model_gru.ipynb` dosyasını oluştur ve içine şu hücreleri ekle:
   - **Hücre 1 (Kurulum):**
     ```python
     %load_ext autoreload
     %autoreload 2
     import sys; sys.path.append('..')
     import torch
     import pickle
     from src.models import GRUModel  # ← LSTM yerine GRU import ediliyor
     from src.train import train_model
     from src.evaluate import evaluate_model, plot_predictions, plot_loss

     device = "cuda" if torch.cuda.is_available() else "cpu"
     print(f"Cihaz: {device}")
     ```
   - **Hücre 2 (Veri Yükleme):** `data/processed/amzn_processed.pt` içindeki train/test tensorlerini yükle ve `scaler.pkl` dosyasını pickle ile oku.
   - **Hücre 3 (Model Kurulumu):** `GRUModel` modelini tanımla ve toplam parametre sayısını yazdır.
   - **Hücre 4 (Eğitim):** Birebir aynı parametrelerle (`epochs=100`, `lr=0.001`, `device=device`) GRU modelini eğit.
   - **Hücre 5 (Değerlendirme):** `evaluate_model` ile test setinde tahmin üret ve bunları dolar cinsine geri dönüştür. MSE ve RMSE değerlerini ekrana yazdır.
   - **Hücre 6 (Grafikler):** Tahmin grafiğini ve eğitim loss eğrisini çizip `outputs/figures/gru_predictions.png` ve `outputs/figures/gru_loss.png` olarak kaydet.
   - **Hücre 7 (Model Kaydı):** Modeli ve eğitim metriklerini `outputs/models/gru_epoch100.pth` dosyasına kaydet:
     ```python
     torch.save({
         'model_state_dict': model.state_dict(),
         'hidden_size': 50,
         'num_layers': 2,
         'mse': mse,
         'rmse': rmse,
         'train_time': train_time,
     }, "../outputs/models/gru_epoch100.pth")
     ```

2. Çalışma tamamlandığında Orkestratör Ajanına bilgi ver.
```

---

## 🧪 3. Test Ajanı Promptu
> **Görevi:** GRU notebook'unun çalışmasını, model ağırlıklarını ve çıktı grafiklerini doğrulamak.

```text
Sen Test Ajanısın. Faz 5 doğrulaması için şu adımları çalıştır:

1. `outputs/models/gru_epoch100.pth` dosyasının dizinde oluştuğunu ve boş olmadığını kontrol et.
2. `outputs/figures/gru_predictions.png` ve `outputs/figures/gru_loss.png` grafik dosyalarının oluştuğunu kontrol et.
3. `notebooks/04_model_gru.ipynb` notebook'unu otomatik olarak baştan sona çalıştırarak test et:
   `jupyter nbconvert --to notebook --execute notebooks/04_model_gru.ipynb --inplace`
4. Kaydedilen model checkpoint dosyasını yükleyip içindeki değerleri doğrulamak için şu scripti çalıştır:
   ```python
   import torch
   ckpt = torch.load("outputs/models/gru_epoch100.pth", map_location="cpu")
   assert 'model_state_dict' in ckpt, "Checkpoint içinde model ağırlıkları yok!"
   assert ckpt['num_layers'] == 2, "Model katman sayısı uyuşmuyor!"
   print(f"✅ GRU Test Başarılı. RMSE: {ckpt['rmse']:.4f} $")
   ```

Sonuçları Orkestratör Ajanına raporla.
```
