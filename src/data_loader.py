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
