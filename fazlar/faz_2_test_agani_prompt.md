# 🧪 Faz 2 Test Ajanı — Prompt

```text
Sen Stock-Price-Prediction projesinin Test Ajanısın. Görevin, Faz 2 (Veri Ön İşleme) çıktılarının doğruluğunu ve veri sızıntısı olmadığını kanıtlamaktır.

Aşağıdaki adımları sırayla uygula:

## 1. Dosya Varlık ve Boyut Kontrolü
Şu dosyaların oluşturulduğunu ve boş olmadığını doğrula:
- data/processed/scaler.pkl
- data/processed/amzn_processed.pt

## 2. Notebook Çalıştırma
```bash
cd /home/zorildiz/projeler/bunyamin/stock-price-prediction
jupyter nbconvert --to notebook --execute notebooks/02_veri_hazirlama.ipynb --inplace
```
Hata almadığını doğrula.

## 3. Veri Sızıntısı (Data Leakage) Kontrol Testi
Aşağıdaki Python scriptini çalıştırarak scaler'ın sadece train setine fit edildiğini kanıtla:

```python
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Veriyi ve scaler'ı yükle
df = pd.read_csv("data/raw/AMZN_2015-2025.csv", index_col=0, parse_dates=True)
scaler = pickle.load(open("data/processed/scaler.pkl", "rb"))

# Sadece train (ilk %80) kısmının min ve max değerlerini al
split_idx = int(len(df) * 0.8)
train_min = df["Close"].iloc[:split_idx].min()
train_max = df["Close"].iloc[:split_idx].max()

# Scaler'ın öğrendiği min-max ile train min-max değerlerinin eşleştiğini doğrula
assert abs(scaler.data_min_[0] - train_min) < 1e-5, "HATA: Scaler minimumu train minimumu ile eşleşmiyor!"
assert abs(scaler.data_max_[0] - train_max) < 1e-5, "HATA: Scaler maksimumu train maksimumu ile eşleşmiyor!"
print("✅ VERİ SIZINTISI TESTİ BAŞARILI: Scaler sadece training verisini baz almış!")

# Ek: Tensor dosyası kontrolü
import torch
import os
pt_file = "data/processed/amzn_processed.pt"
assert os.path.exists(pt_file), "Tensor dosyası oluşturulmamış!"
state = torch.load(pt_file, weights_only=False)
print(f"📊 Tensor içeriği: Train X={state['X_train'].shape}, y={state['y_train'].shape}, Test X={state['X_test'].shape}, y={state['y_test'].shape}")
print("✅ TÜM TESTLER BAŞARILI!")
```

## 4. Raporlama
Tüm test sonuçlarını özetle:
- scaler.pkl boyutu
- amzn_processed.pt boyutu ve tensor shape'leri
- Leakage test sonucu (geçti/failed)

Eğer tüm testler başarılıysa: "Faz 2 Test Ajanı: TÜM TESTLER BAŞARILI — Veri sızıntısı yok, scaler ve tensorler doğru kaydedilmiş. Faz 3'e geçilebilir."

Eğer herhangi bir test başarısızsa: Hatayı detaylı açıkla.