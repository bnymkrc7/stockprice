"""
src/preprocessing.py — Veri Ön İşleme ve Feature Engineering

TradingView indikatörlerini destekler.
MinMaxScaler ile veri ölçekleme, sequence oluşturma ve tensor hazırlama.

Veri sızıntısını (Data Leakage) önlemek için scaler sadece train verisine fit edilir.
"""

import numpy as np
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from .tradingview_features import (
    fetch_tradingview_indicators,
    prepare_tradingview_features,
    create_sequences_with_indicators,
)


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


def scale_multi_features(
    df: pd.DataFrame,
    columns: list,
    train_ratio: float = 0.8,
    feature_range: tuple = (-1, 1),
) -> tuple:
    """
    Çoklu feature'ları scaler ile ölçekler.

    Args:
        df: OHLCV + indikatör sütunları olan DataFrame
        columns: Ölçeklenecek sütun listesi
        train_ratio: Eğitim/test split oranı
        feature_range: Ölçek aralığı

    Returns:
        tuple: (scaled_array, scaler)
    """
    split_idx = int(len(df) * train_ratio)
    scaler = MinMaxScaler(feature_range=feature_range)

    # Sadece train verisine fit (veri sızıntısını önle!)
    scaler.fit(df[columns].iloc[:split_idx])
    scaled = scaler.transform(df[columns])
    return scaled, scaler


def create_sequences(data: np.ndarray, lookback: int = 20) -> tuple:
    """Kayan pencere (sliding window) ile sequence verisi oluşturur."""
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i - lookback:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def create_sequences_multi(
    data: np.ndarray,
    lookback: int = 20,
    target_columns: list = None,
) -> tuple:
    """
    Çoklu feature ile sequence verisi oluşturur.

    Args:
        data: Scaled feature matrix (n_samples, n_features)
        lookback: Pencere boyutu
        target_columns: Hedef sütun indeksleri (opsiyonel, varsayılan: son sütun)

    Returns:
        tuple: (X, y) — X: (n_samples, lookback, n_features), y: (n_samples, target)
    """
    X, y = [], []
    n_features = data.shape[1]

    if target_columns is None:
        target_columns = [n_features - 1]  # Son sütun (Close)

    for i in range(lookback, len(data)):
        X.append(data[i - lookback:i, :])  # Tüm feature'ları al
        y.append(data[i, target_columns])  # Hedef sütunları al

    return np.array(X), np.array(y)


def prepare_tensors(X: np.ndarray, y: np.ndarray,
                    train_ratio: float = 0.8,
                    device: str = "cpu") -> tuple:
    """Verileri PyTorch float tensorlerine çevirir ve train/test split yapar."""
    split = int(len(X) * train_ratio)

    # LSTM için 3D şekil: (batch, seq_len, input_size) -> unsqueeze(-1) ekliyoruz
    X_train = torch.from_numpy(X[:split]).float().unsqueeze(-1)
    y_train = torch.from_numpy(y[:split]).float().unsqueeze(-1)
    X_test = torch.from_numpy(X[split:]).float().unsqueeze(-1)
    y_test = torch.from_numpy(y[split:]).float().unsqueeze(-1)

    print(f"📊 Tensorler Hazırlandı:")
    print(f"   Train set: X={X_train.shape}, y={y_train.shape}")
    print(f"   Test set:  X={X_test.shape}, y={y_test.shape}")

    return (X_train.to(device), y_train.to(device)), \
           (X_test.to(device), y_test.to(device))


def prepare_tensors_multi(
    X: np.ndarray,
    y: np.ndarray,
    train_ratio: float = 0.8,
    device: str = "cpu",
) -> tuple:
    """
    Çoklu feature tensorlerini hazırlar.
    X zaten 3D (batch, seq_len, features) olduğu için unsqueeze gerekmez.
    """
    split = int(len(X) * train_ratio)

    X_train = torch.from_numpy(X[:split]).float()
    y_train = torch.from_numpy(y[:split]).float()
    X_test = torch.from_numpy(X[split:]).float()
    y_test = torch.from_numpy(y[split:]).float()

    print(f"📊 Multi-Feature Tensorler Hazırlandı:")
    print(f"   Train set: X={X_train.shape}, y={y_train.shape}")
    print(f"   Test set:  X={X_test.shape}, y={y_test.shape}")

    return (X_train.to(device), y_train.to(device)), \
           (X_test.to(device), y_test.to(device))


def prepare_tradingview_data(
    raw_df: pd.DataFrame,
    symbol: str = "NASDAQ:AMZN",
    lookback: int = 20,
    device: str = "cpu",
) -> tuple:
    """
    TradingView indikatörlerini yükleyip, scaler ile ölçekleyip,
    sequence oluşturur — tüm pipeline bir fonksiyonda.

    Args:
        raw_df: Orijinal OHLCV verisi (yfinance'den)
        symbol: TradingView sembolü
        lookback: Pencere boyutu
        device: PyTorch device

    Returns:
        tuple: ((X_train, y_train), (X_test, y_test))
    """
    # 1. TradingView indikatörlerini çek
    print(f"📡 TradingView indikatörleri çekiliyor ({symbol})...")
    indicators = fetch_tradingview_indicators(symbol=symbol)
    print(f"   İndikatörler: {list(indicators.columns)}")

    # 2. OHLCV + İndikatörleri birleştir ve scaler ile ölçekle
    print("📏 Feature'lar ölçekleniyor...")
    scaled, scaler = prepare_tradingview_features(raw_df, indicators, fit_only=True)

    # 3. Sequence oluştur (lookback penceresi)
    print(f"🔄 Sequence verisi oluşturuluyor (lookback={lookback})...")
    X, y = create_sequences_with_indicators(scaled, lookback=lookback)

    # 4. Tensor hazırla (scaler leakage koruması zaten yapıldı)
    print("🔢 Tensorler hazırlanıyor...")
    (X_train, y_train), (X_test, y_test) = prepare_tensors_multi(X, y, device=device)

    return (X_train, y_train), (X_test, y_test), scaler
