"""
src/tradingview_features.py — TradingView Teknik İndikatör Entegrasyonu

TradingView Ta (tradingview_ta) kütüphanesi üzerinden teknik indikatörleri çeker.
İndikatörler: RSI, MACD, SMA20, Volume, Bollinger Bands

Veri sızıntısını önlemek için scaler sadece training setine fit edilir.
"""

import numpy as np
import pandas as pd
import tradingview_ta as ta
from tradingview_ta import TA_Handler, Interval


def fetch_tradingview_indicators(
    symbol: str = "NASDAQ:AMZN",
    interval: str = Interval.INTERVAL_1_DAY,
) -> pd.DataFrame:
    """
    TradingView API üzerinden teknik indikatörleri çeker.

    Args:
        symbol: TradingView sembolü (örn: "NASDAQ:AMZN", "NYSE:MSFT")
        interval: Zaman dilimi (daily, hourly vb.)

    Returns:
        pd.DataFrame — OHLCV verisi + teknik indikatör sütunları
    """
    handler = TA_Handler(
        symbol=symbol,
        screener="america",
        exchange="NASDAQ",
        interval=interval,
    )
    df = handler.get_analysis()

    # Sütun isimlerini Türkçe açıklamalarla birleştir
    indicator_columns = {
        "RSI": df.get_indicators()["RSI"],
        "MACD.macd": df.get_indicators()["MACD.macd"],
        "MACD.signal": df.get_indicators()["MACD.signal"],
        "SMA20": df.get_indicators()["SMA20"],
        "EMA20": df.get_indicators()["EMA20"],
        "Bollinger_Bands.upper": df.get_indicators()["Bollinger_Bands.upper"],
        "Bollinger_Bands.lower": df.get_indicators()["Bollinger_Bands.lower"],
        "Volume": df.get_indicators()["Volume"],
    }

    result = pd.DataFrame([indicator_columns])
    result.index = ["indikatörler"]
    return result


def get_multiple_indicators(
    symbol: str = "NASDAQ:AMZN",
    periods: list = None,
    interval: str = Interval.INTERVAL_1_DAY,
) -> pd.DataFrame:
    """
    Birden fazla periyot için teknik indikatörleri çeker.

    Args:
        symbol: TradingView sembolü
        periods: Periyot listesi (örn: [1, 5, 10, 20, 50])
        interval: Zaman dilimi

    Returns:
        pd.DataFrame — her periyot için indikatör değerleri
    """
    if periods is None:
        periods = [1, 5, 10, 20, 50]

    results = []
    for p in periods:
        handler = TA_Handler(
            symbol=symbol,
            screener="america",
            exchange="NASDAQ",
            interval=interval,
        )
        analysis = handler.get_analysis()
        indicators = analysis.get_indicators()

        row = {
            "periyot": p,
            "RSI": indicators.get("RSI"),
            "MACD": indicators.get("MACD.macd"),
            "MACD_Signal": indicators.get("MACD.signal"),
            "SMA20": indicators.get("SMA20"),
            "EMA20": indicators.get("EMA20"),
            "BB_Upper": indicators.get("Bollinger_Bands.upper"),
            "BB_Lower": indicators.get("Bollinger_Bands.lower"),
            "Volume": indicators.get("Volume"),
        }
        results.append(row)

    return pd.DataFrame(results)


def prepare_tradingview_features(
    raw_df: pd.DataFrame,
    indicators_df: pd.DataFrame,
    scaler=None,
    fit_only: bool = True,
) -> tuple:
    """
    TradingView indikatörlerini OHLCV verisiyle birleştirir ve scaler ile ölçekler.

    Veri sızıntısını önlemek için scaler sadece training setine fit edilir.

    Args:
        raw_df: Orijinal OHLCV DataFrame
        indicators_df: TradingView indikatörleri DataFrame
        scaler: Optional — mevcut scaler (test verisi için transform)
        fit_only: True ise scaler sadece train verisine fit edilir

    Returns:
        tuple: (scaled_features, scaler veya None)
    """
    # OHLCV sütunlarını seç
    ohlcv = raw_df[["Open", "High", "Low", "Close", "Volume"]].copy()

    # İndikatör sütunlarını ekle (NaN varsa 0 ile doldur)
    indicator_cols = indicators_df.columns.tolist()
    for col in indicator_cols:
        ohlcv[col] = indicators_df[col].values

    # Veri sızıntısını önle: scaler sadece train verisine fit edilir
    split_idx = int(len(ohlcv) * 0.8)

    if scaler is None or fit_only:
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler.fit(ohlcv.iloc[:split_idx])

    scaled = scaler.transform(ohlcv)
    return scaled, scaler


def create_sequences_with_indicators(
    data: np.ndarray,
    lookback: int = 20,
) -> tuple:
    """
    Kayan pencere ile sequence verisi oluşturur — çoklu indikatörlerle.

    Args:
        data: Scaled feature matrix (n_samples, n_features)
        lookback: Pencere boyutu

    Returns:
        tuple: (X, y) — X: (n_samples, lookback, n_features), y: (n_samples, n_features)
    """
    X, y = [], []
    n_features = data.shape[1]

    for i in range(lookback, len(data)):
        X.append(data[i - lookback:i, :])  # Tüm feature'ları al
        y.append(data[i, :])  # Tüm feature'ları hedef olarak al (close + indikatörler)

    return np.array(X), np.array(y)
