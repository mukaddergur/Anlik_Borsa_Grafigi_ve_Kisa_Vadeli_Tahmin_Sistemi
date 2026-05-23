import pandas as pd
import yfinance as yf

def get_live_data(symbol):
    """Son 1 günlük, 1 dakikalık periyotlarla canlı veri çeker."""
    data = yf.download(
        tickers=symbol,
        period="1d",
        interval="1m",
        progress=False
    )
    if data.empty:
        return pd.DataFrame()
    
    data = data.reset_index()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if col[1] == '' else col[0] for col in data.columns]
    return data

def get_historical_data(symbol):
    """Model eğitimi için son 90 günlük günlük veriyi çeker."""
    data = yf.download(
        tickers=symbol,
        period="90d",
        interval="1d",
        progress=False
    )
    if data.empty:
        return pd.DataFrame()
    
    data = data.reset_index()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if col[1] == '' else col[0] for col in data.columns]
    return data