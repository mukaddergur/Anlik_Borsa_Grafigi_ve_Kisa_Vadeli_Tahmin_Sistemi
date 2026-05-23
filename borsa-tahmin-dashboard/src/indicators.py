import pandas as pd
import numpy as np

def prepare_features(df):
    df = df.copy()

    df["Daily_Return"] = df["Close"].pct_change()
    df["MA_7"] = df["Close"].rolling(window=7).mean()
    df["MA_14"] = df["Close"].rolling(window=14).mean()
    df["MA_30"] = df["Close"].rolling(window=30).mean()
    df["Volatility_7"] = df["Daily_Return"].rolling(window=7).std()
    df["Volume_Change"] = df["Volume"].pct_change()
    df["Price_Range"] = (df["High"] - df["Low"]) / df["Close"]
    df["Target"] = df["Close"].shift(-1)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    return df