import pandas as pd
import numpy as np

def moving_average(df, window):
    return df["Close"].rolling(window=window).mean()

def rsi(df, window=14):
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(df, fast=12, slow=26, signal=9):
    ema_fast = df["Close"].ewm(span=fast, min_periods=fast).mean()
    ema_slow = df["Close"].ewm(span=slow, min_periods=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, min_periods=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def bollinger_bands(df, window=20, num_std=2):
    rolling_mean = df["Close"].rolling(window).mean()
    rolling_std = df["Close"].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

def add_indicators(df):
    df["ma5"] = moving_average(df, 5)
    df["ma20"] = moving_average(df, 20)
    df["rsi"] = rsi(df)
    macd_line, signal_line, hist = macd(df)
    df["macd"] = macd_line
    df["signal_line"] = signal_line
    df["histogram"] = hist
    mid, upper, lower = bollinger_bands(df)
    df["bb_mid"] = mid
    df["bb_upper"] = upper
    df["bb_lower"] = lower
    return df.dropna()
