# 🟢 Faz 2: Veri Ön İşleme (Veri Sızıntısız) — Ajan Promptları

Bu dosya, projenin ikinci aşaması (Faz 2 - Veri Ön İşleme) için Kodlama, Test ve Kontrol ajanlarının promptlarını içerir. Bu aşamada veri sızıntısını (data leakage) engellemek kritik önem taşımaktadır.

---

## 1. 🛡️ Kontrol/Orkestratör Ajan Promptu
> **Görevi:** Veri ön işleme aşamasında veri sızıntısının (data leakage) engellendiğini denetlemek ve veri hazırlığı notebook'unu koordine etmek.

```text
Sen Stock-Price-Prediction projesinin Kontrol/Orkestratör Ajanısın. Görevin Faz 2 (Veri Ön İşleme) aşamasını koordine etmektir.

Adımlar:
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki Faz 2 görevlerini `[/]` (devam ediyor) olarak işaretlesin.
2. Geliştirici Ajanın yazacağı src/preprocessing.py kodunda MinMaxScaler fit işleminin sadece train seti üzerinde yapıldığını (test setinin sızmadığını) kontrol et.
3. 02_veri_hazirlama.ipynb notebook dosyasının oluşturulması görevini ver.
4. Test Ajanına, üretilen verilerin boyutlarını, scaler nesnesini ve veri sızıntısı kontrol testlerini doğrulama görevi ver.
5. Test raporu başarılıysa, `fazlar/TASKS.md` dosyasındaki ilgili görevleri `[x]` (tamamlandı) yap, kullanıcıya bildir ve Faz 3'e geçişi başlatın.
```

---

## 2. 💻 Kodlama Ajanı Promptu
> **Görevi:** Veri sızıntısız `src/preprocessing.py` yazmak ve `notebooks/02_veri_hazirlama.ipynb` notebook'unu oluşturmak.

```text
Sen Geliştirici Ajansın. Faz 2 kapsamında veri sızıntısını engelleyecek şekilde aşağıdaki adımları tamamla:

1. `src/preprocessing.py` dosyasını oluştur ve içine şu kodları yaz:
   ```python
   import numpy as np
   import torch
   import pandas as pd
   from sklearn.preprocessing import MinMaxScaler

   def scale_data(df: pd.DataFrame, column: str = "Close",
                  train_ratio: float = 0.8,
                  feature_range: tuple = (-1, 1)) -> tuple:
       """
       Veriyi [-1, 1] aralığına ölçekler.
       VERİ SIZINTISINI (Data Leakage) önlemek için fit işlemi sadece train verisi üzerinde yapılır.
       """
       split_idx = int(len(df) * train_ratio)
       scaler = MinMaxScaler(feature_range=feature_range)
       
       # Scaler sadece eğitim setindeki fiyatlara fit edilir (Leakage engelleme!)
       scaler.fit(df[[column]].iloc[:split_idx])
       
       # Tüm veri seti, train setine göre eğitilmiş olan bu scaler ile dönüştürülür
       scaled = scaler.transform(df[[column]])
       return scaled, scaler

   def create_sequences(data: np.ndarray, lookback: int = 20) -> tuple:
       """Kayan pencere (sliding window) ile sequence verisi oluşturur."""
       X, y = [], []
       for i in range(lookback, len(data)):
           X.append(data[i-lookback:i, 0])
           y.append(data[i, 0])
       return np.array(X), np.array(y)

   def prepare_tensors(X: np.ndarray, y: np.ndarray,
                       train_ratio: float = 0.8,
                       device: str = "cpu") -> tuple:
       """Verileri PyTorch float tensorlerine çevirir ve train/test split yapar."""
       split = int(len(X) * train_ratio)
       
       # LSTM için 3D şekil: (batch, seq_len, input_size) -> unsqueeze(-1) ekliyoruz
       X_train = torch.from_numpy(X[:split]).float().unsqueeze(-1)
       y_train = torch.from_numpy(y[:split]).float().unsqueeze(-1)
       X_test  = torch.from_numpy(X[split:]).float().unsqueeze(-1)
       y_test  = torch.from_numpy(y[split:]).float().unsqueeze(-1)
       
       print(f"📊 Tensorler Hazırlandı:")
       print(f"   Train set: X={X_train.shape}, y={y_train.shape}")
       print(f"   Test set:  X={X_test.shape}, y={y_test.shape}")
       
       return (X_train.to(device), y_train.to(device)), \
              (X_test.to(device), y_test.to(device))
   ```

2. `notebooks/02_veri_hazirlama.ipynb` notebook dosyasını oluştur ve hücre hücre şunları ekle:
   - **Hücre 1:** Importlar ve veri yükleme (`data/raw/AMZN_2015-2025.csv`).
   - **Hücre 2:** `scale_data` çağrısı, orijinal fiyat sınırları ile scaled fiyat sınırlarını yazdır.
   - **Hücre 3:** `create_sequences` (lookback=20) çağrısı.
   - **Hücre 4:** `prepare_tensors` çağrısı.
   - **Hücre 5 (Kayıt):** Scaler nesnesini `pickle` ile `data/processed/scaler.pkl` dosyasına kaydet. Tensorleri `torch.save` ile `data/processed/amzn_processed.pt` olarak kaydet.

3. İşlem tamamlandığında Orkestratör Ajanına rapor ver.
```

---

## 🧪 3. Test Ajanı Promptu
> **Görevi:** Veri sızıntısı olmadığını, scaler ve tensorlerin düzgün kaydedildiğini doğrulamak.

```text
Sen Test Ajanısın. Faz 2 doğrulaması için şu adımları çalıştır:

1. `data/processed/scaler.pkl` ve `data/processed/amzn_processed.pt` dosyalarının oluştuğunu ve boş olmadığını kontrol et.
2. `notebooks/02_veri_hazirlama.ipynb` notebook'unu çalıştır ve hata almadığını doğrula:
   `jupyter nbconvert --to notebook --execute notebooks/02_veri_hazirlama.ipynb --inplace`

3. **Veri Sızıntısı (Data Leakage) Kontrol Testi:**
   Python konsolunda, test setindeki verilerin min ve max değerlerinin scaler parametrelerini (`data_min_`, `data_max_`) etkilemediğini doğrulayan bir script çalıştır:
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
   ```

Sonuçları Orkestratör Ajanına raporla.
```
