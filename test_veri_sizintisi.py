import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch
import os

os.chdir("/home/zorildiz/projeler/bunyamin/stock-price-prediction")

print("=== 1. Dosya Kontrolü ===")
pkl_size = os.path.getsize("data/processed/scaler.pkl")
pt_size = os.path.getsize("data/processed/amzn_processed.pt")
assert pkl_size > 0, "scaler.pkl boş!"
assert pt_size > 0, "amzn_processed.pt boş!"
print(f"scaler.pkl: {pkl_size} byte")
print(f"amzn_processed.pt: {pt_size} byte")

print("\n=== 2. VERİ SIZINTISI TESTİ ===")
df = pd.read_csv("data/raw/AMZN_2015-2025.csv", index_col=0, parse_dates=True)
scaler = pickle.load(open("data/processed/scaler.pkl", "rb"))

split_idx = int(len(df) * 0.8)
train_min = df["Close"].iloc[:split_idx].min()
train_max = df["Close"].iloc[:split_idx].max()

print(f"Train set min: {train_min}")
print(f"Train set max: {train_max}")
print(f"Scaler data_min_: {scaler.data_min_[0]}")
print(f"Scaler data_max_: {scaler.data_max_[0]}")

assert abs(scaler.data_min_[0] - train_min) < 1e-5, "HATA: Scaler minimumu train minimumu ile eşleşmiyor!"
assert abs(scaler.data_max_[0] - train_max) < 1e-5, "HATA: Scaler maksimumu train maksimumu ile eşleşmiyor!"
print("VERİ SIZINTISI TESTİ BAŞARILI: Scaler sadece training verisini baz almış!")

print("\n=== 3. TENSOR DOSYA KONTROLÜ ===")
state = torch.load("data/processed/amzn_processed.pt", weights_only=False)
print(f"Train X: {state['X_train'].shape}")
print(f"Train y: {state['y_train'].shape}")
print(f"Test  X: {state['X_test'].shape}")
print(f"Test  y: {state['y_test'].shape}")
print("Tensor dosyası okunabilir ve shape'ler uygun.")

print("\nTUM TESTLER BASARILI!")
