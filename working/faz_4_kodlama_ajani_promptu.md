# 💻 GELİŞTİRİCİ GÖREVİ: FAZ_4 — LSTM Eğitimi (Süre: ~2-3 saat)

## 🎯 GÖREV DETAYLARI (PLANDAN OKUNAN)
> **Ne yapacağız:** LSTM modelini kur, eğit, değerlendir. İlk gerçek modelin olacak! 🎉

### 📓 Notebook: `03_model_lstm.ipynb`

**Hücre 1:** Setup
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
print(f"Kullanılan cihaz: {device}")
```

**Hücre 2:** Veriyi yükle
```python
data = torch.load("../data/processed/amzn_processed.pt", weights_only=True, map_location=device)
scaler = pickle.load(open("../data/processed/scaler.pkl", "rb"))

X_train, y_train = data['X_train'], data['y_train']
X_test, y_test = data['X_test'], data['y_test']
```

**Hücre 3:** Modeli oluştur
```python
model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)
print(f"📐 Parametre sayısı: {sum(p.numel() for p in model.parameters()):,}")
```

📌 **Parametre sayısı neden önemli?** Çok parametre = yüksek kapasite ama overfitting riski. 50 hidden × 2 layer LSTM için yaklaşık 40K parametre — bu ölçekte bir veri için makul.

**Hücre 4:** Eğit
```python
loss_history, train_time = train_model(
    model, X_train, y_train,
    epochs=100, lr=0.001, device=device
)
```

**Hücre 5:** Değerlendir
```python
preds, actuals, mse, rmse = evaluate_model(
    model, X_test, y_test, scaler=scaler, device=device
)

plot_predictions(actuals, preds,
    title="LSTM: Amazon Hisse Fiyat Tahmini",
    save_path="../outputs/figures/lstm_predictions.png")

plot_loss(loss_history,
    title="LSTM Eğitim Kaybı",
    save_path="../outputs/figures/lstm_loss.png")
```

**Hücre 6:** Modeli kaydet
```python
torch.save({
    'model_state_dict': model.state_dict(),
    'hidden_size': 50,
    'num_layers': 2,
    'mse': mse,
    'rmse': rmse,
    'train_time': train_time,
}, "../outputs/models/lstm_epoch100.pth")
print(f"💾 Model kaydedildi: outputs/models/lstm_epoch100.pth")
```

---

## 🔄 GELİŞTİRİCİ İŞ AKIŞI
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki FAZ_4 görevini `[/]` (devam ediyor) olarak işaretlesin.
2. Yukarıda belirtilen kodlama hedeflerini, modülerlik ve veri sızıntısını önleme kurallarına uyarak kodlayın.
3. Çalışma bittiğinde `working/done_faz_4.md` adında bir done dosyası oluşturarak yapılan işleri özetleyin.
4. Değişikliklerinizi test ajanı ile doğrulamaya hazır hale getirin.
