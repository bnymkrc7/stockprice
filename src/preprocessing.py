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
