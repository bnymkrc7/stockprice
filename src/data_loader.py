"""
src/data_loader.py — Veri Yükleme ve TradingView API Entegrasyonu

Mevcut yfinance tabanlı veri indirme fonksiyonlarını korur.
TradingView API'den teknik indikatör verisi çekme fonksiyonları eklenmiştir.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path


def fetch_stock_data(ticker: str = "AMZN",
                     start: str = "2015-01-01",
                     end: str = "2025-01-01",
                     save_path: str = None) -> pd.DataFrame:
    """yfinance ile market verisi indirir ve MultiIndex sütunları düzleştirir."""
    print(f"📥 {ticker} verisi indiriliyor ({start} - {end})...")
    df = yf.download(ticker, start=start, end=end, progress=True)

    # Sütunlar MultiIndex ise level 0'ı seçip düzleştir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    print(f"✅ {len(df)} satır veri hazır.")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path)
        print(f"💾 Kaydedildi: {save_path}")

    return df


def load_local_data(path: str) -> pd.DataFrame:
    """Yerel CSV dosyasını yükler."""
    return pd.read_csv(path, index_col=0, parse_dates=True)


def fetch_tradingview_stock_data(
    symbol: str = "NASDAQ:AMZN",
    start: str = "2015-01-01",
    end: str = "2025-01-01",
) -> pd.DataFrame:
    """
    TradingView API'den hisse senedi verisi çeker.

    TradingView Ta (tradingview_ta) kütüphanesi üzerinden
    OHLCV verisi ve teknik indikatörleri tek seferde alır.

    Args:
        symbol: TradingView sembolü (örn: "NASDAQ:AMZN")
        start: Başlangıç tarihi
        end: Bitiş tarihi

    Returns:
        pd.DataFrame — OHLCV + teknik indikatör verisi
    """
    import tradingview_ta as ta
    from tradingview_ta import TA_Handler, Interval

    print(f"📡 TradingView'dan {symbol} verisi çekiliyor ({start} - {end})...")

    # OHLCV verisi için yfinance kullan (TradingView TA OHLCV tarihli veri sağlamaz)
    yf_ticker = symbol.split(":")[1] if ":" in symbol else symbol
    ohlcv_df = yf.download(yf_ticker, start=start, end=end, progress=True)

    if isinstance(ohlcv_df.columns, pd.MultiIndex):
        ohlcv_df.columns = ohlcv_df.columns.get_level_values(0)

    # Teknik indikatörleri TradingView API'den çek
    handler = TA_Handler(
        symbol=symbol,
        screener="america",
        exchange=symbol.split(":")[0] if ":" in symbol else "NASDAQ",
        interval=Interval.INTERVAL_1_DAY.value,
    )
    analysis = handler.get_analysis()
    indicators = analysis.get_indicators()

    # OHLCV verisine indikatörleri ekle
    indicator_columns = {
        "RSI": indicators.get("RSI"),
        "MACD": indicators.get("MACD.macd"),
        "MACD_Signal": indicators.get("MACD.signal"),
        "SMA20": indicators.get("SMA20"),
        "EMA20": indicators.get("EMA20"),
        "BB_Upper": indicators.get("Bollinger_Bands.upper"),
        "BB_Lower": indicators.get("Bollinger_Bands.lower"),
        "Volume": indicators.get("Volume"),
    }

    # TradingView indikatörleri tek satır döndürüyor, tüm satırlara yay
    for col, val in indicator_columns.items():
        if val is not None:
            ohlcv_df[col] = val
        else:
            ohlcv_df[col] = 0.0

    print(f"✅ {len(ohlcv_df)} satır veri + {len(indicator_columns)} indikatör hazır.")
    return ohlcv_df
