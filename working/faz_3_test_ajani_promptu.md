# 🧪 TEST AJANI: FAZ_3 — Model Mimarileri — PyTorch (Süre: ~2-3 saat)

## 🎯 TEST VE DOĞRULAMA DETAYLARI (PLANDAN OKUNAN)
> **Ne öğreneceksin:** PyTorch'ta `nn.Module` ile özel model tanımlamayı, LSTM vs GRU farkını, eğitim döngüsünü.

### 🧠 3.1 — Teori: LSTM vs GRU Nedir?

```
RNN (Basit):
  h(t) = tanh(W·x(t) + U·h(t-1))
  ❌ Uzun vadeli bağımlılıkları hatırlayamaz (vanishing gradient)

LSTM (1997):
  + Forget Gate: neyi unutacağını öğrenir
  + Input Gate: neyi hatırlayacağını öğrenir  
  + Output Gate: neyi çıktı olarak vereceğini öğrenir
  ✅ Uzun vadeli (100+ adım) hatırlayabilir
  
GRU (2014):
  - LSTM'in basitleştirilmiş hali (3 gate → 2 gate)
  - Daha az parametre → daha hızlı eğitim
  - Çoğu görevde LSTM'e yakın performans
  ✅ "LSTM'in hızlı kardeşi"
```

📌 **Projemizde:** İkisini de eğitip karşılaştıracağız. Hangisi daha iyi? Tahminin nedir? 😉

### 🐍 3.2 — Kod: `src/models.py`

```python
# src/models.py
import torch.nn as nn

class LSTMModel(nn.Module):
    """
    2 katmanlı LSTM modeli.
    
    Mimarisi:
      Input (batch, 20, 1) 
        → LSTM(hidden=50, layers=2, dropout=0.2) 
        → Linear(50 → 1)
        → Output (batch, 1)
    
    Neden 2 katman? Daha fazla öğrenme kapasitesi.
    Neden dropout=0.2? Overfitting'i önlemek için (nöronların %20'sini rastgele kapatır).
    Neden hidden=50? 20 günlük girdi için yeterli kapasite.
    """
    def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        # x shape: (batch, 20, 1)
        out, _ = self.lstm(x)
        # out shape: (batch, 20, 50) → son adımı al
        return self.fc(out[:, -1, :])
        # çıktı: (batch, 1) — tahmin edilen fiyat

class GRUModel(nn.Module):
    """
    2 katmanlı GRU modeli — LSTM ile aynı parametrelerde.
    """
    def __init__(self, input_size=1, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])
```

📌 **Neden `batch_first=True`?** Girdi boyutu (batch, seq, features) olur. Daha doğal. False olsa (seq, batch, features) olurdu.

📌 **Neden `out[:, -1, :]`?** LSTM her adımda çıktı üretir (20 adım). Son adımın çıktısını alırız çünkü sadece 21. günü tahmin edeceğiz.

### 🐍 3.3 — Kod: `src/train.py`

```python
# src/train.py
import time
import torch
import torch.nn as nn

def train_model(model, X_train, y_train, epochs=100, lr=0.001,
                device="cpu", verbose=True):
    """
    Standart PyTorch eğitim döngüsü.
    
    Adımlar:
    1. forward pass (tahmin yap)
    2. loss hesapla (tahmin ile gerçek arasındaki fark)
    3. backward pass (gradyan hesapla)
    4. optimizer.step() (ağırlıkları güncelle)
    """
    model = model.to(device)
    X_train, y_train = X_train.to(device), y_train.to(device)
    
    criterion = nn.MSELoss()
    # Neden Adam? Adaptive learning rate, genelde SGD'den iyi çalışır
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    loss_history = []
    start_time = time.time()
    
    for epoch in range(epochs):
        model.train()
        
        # Forward
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        
        # Backward
        optimizer.zero_grad()  # Önceki gradyanları sıfırla
        loss.backward()        # Gradyanları hesapla
        optimizer.step()       # Ağırlıkları güncelle
        
        loss_history.append(loss.item())
        
        if verbose and (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] Loss: {loss.item():.6f}")
    
    elapsed = time.time() - start_time
    print(f"✅ Eğitim tamamlandı! Süre: {elapsed:.2f} sn")
    print(f"   Son Loss: {loss_history[-1]:.6f}")
    
    return loss_history, elapsed
```

📌 **Dikkat:** `optimizer.zero_grad()` çok önemli! Her epoch'ta gradyanlar birikir, sıfırlamazsan loss hep aynı kalır.

### 🐍 3.4 — Kod: `src/evaluate.py`

```python
# src/evaluate.py
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def evaluate_model(model, X_test, y_test, scaler=None, device="cpu"):
    """
    Modeli test verisinde değerlendirir.
    
    Metrikler:
    - MSE: Ortalama Kare Hata (büyük hataları cezalandırır)
    - RMSE: Karekök MSE (dolar cinsinden hata)
    """
    model.eval()
    X_test, y_test = X_test.to(device), y_test.to(device)
    
    with torch.no_grad():
        predictions = model(X_test)
    
    # CPU'ya al ve numpy'e çevir
    preds = predictions.cpu().numpy()
    actuals = y_test.cpu().numpy()
    
    # Eğer scaler varsa, orijinal fiyata geri çevir
    if scaler:
        preds = scaler.inverse_transform(preds)
        actuals = scaler.inverse_transform(actuals)
    
    # Metrikler
    mse = mean_squared_error(actuals, preds)
    rmse = np.sqrt(mse)
    
    print(f"📊 Model Değerlendirme:")
    print(f"   MSE : {mse:.4f}")
    print(f"   RMSE: {rmse:.4f} $")
    
    return preds, actuals, mse, rmse

def plot_predictions(actuals, preds, title="Gerçek vs Tahmin", save_path=None):
    """Gerçek fiyatlar ile tahminleri karşılaştırmalı gösterir."""
    plt.figure(figsize=(14, 5))
    plt.plot(actuals, label='Gerçek Fiyat', linewidth=1.5, alpha=0.8)
    plt.plot(preds, label='Tahmin', linewidth=1.5, alpha=0.8)
    plt.title(title)
    plt.xlabel('Gün')
    plt.ylabel('Fiyat ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()

def plot_loss(loss_history, title="Eğitim Kaybı", save_path=None):
    """Loss eğrisini çizer — modelin öğrenip öğrenmediğini gösterir."""
    plt.figure(figsize=(10, 4))
    plt.plot(loss_history, linewidth=1)
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
```

📌 **Loss eğrisi ne anlatır?**
- 📉 **Düzenli düşüyor** → Model öğreniyor ✅
- 📈 **Yükseliyor** → Learning rate çok yüksek, patlıyor
- ➡️ **Düzleşiyor** → Model doyuma ulaştı, daha fazla epoch anlamsız
- 📊 **Train düşer test yükselir** → Overfitting (ezberleme) ⚠️

---

## 📋 TEST UYGULAMA TALİMATLARI
1. Kodlama aşamasında yazılan/değiştirilen tüm dosyaların yerlerin olduğunu doğrulayın.
2. İlgili test senaryolarını çalıştırın (örneğin import testleri, model ileri besleme testleri veya veri doğrulama testleri).
3. Test çıktılarında herhangi bir `WARNING` veya `HATA` olmadığından emin olun (oturum bulunamadığında graceful fallback kullanın).
4. Test sonuçlarını `working/test_report_faz_3.md` dosyası olarak kaydedin.
5. Başarılı sonuçları Orkestratör Ajanına rapor edin.
