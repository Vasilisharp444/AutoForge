"""Data loading and indicator computation."""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_csv(path, datetime_col="DateTime", sort=True):
    """Load OHLCV CSV. Returns DataFrame with standard column names."""
    df = pd.read_csv(path, parse_dates=[datetime_col])
    df = df.rename(columns={datetime_col: "DateTime"})
    required = {"DateTime", "Open", "High", "Low", "Close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if "Volume" not in df.columns:
        df["Volume"] = 0
    if sort:
        df = df.sort_values("DateTime").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Individual indicators
# ---------------------------------------------------------------------------

def sma(series, period):
    return series.rolling(period).mean()


def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def bollinger(series, period, std_dev=2.0, ddof=1):
    """Bollinger Bands with sample std (ddof=1) by default."""
    mid = series.rolling(period).mean()
    sd = series.rolling(period).std(ddof=ddof)
    upper = mid + std_dev * sd
    lower = mid - std_dev * sd
    return mid, upper, lower


def atr(df, period):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def slope(series, lookback):
    """Simple slope: (current - lookback bars ago) / lookback."""
    return (series - series.shift(lookback)) / lookback


def vwap(df):
    """Session VWAP. Assumes data is within a single session or caller handles resets."""
    typical = (df["High"] + df["Low"] + df["Close"]) / 3
    cum_vol = df["Volume"].cumsum()
    cum_tp_vol = (typical * df["Volume"]).cumsum()
    return cum_tp_vol / cum_vol


# ---------------------------------------------------------------------------
# Indicator dispatcher
# ---------------------------------------------------------------------------

INDICATOR_REGISTRY = {
    "sma": lambda df, p: sma(df[p.get("source", "Close")], p["period"]),
    "ema": lambda df, p: ema(df[p.get("source", "Close")], p["period"]),
    "rsi": lambda df, p: rsi(df[p.get("source", "Close")], p["period"]),
    "bb_mid": lambda df, p: bollinger(df[p.get("source", "Close")], p["period"], p.get("std", 2.0), p.get("ddof", 1))[0],
    "bb_upper": lambda df, p: bollinger(df[p.get("source", "Close")], p["period"], p.get("std", 2.0), p.get("ddof", 1))[1],
    "bb_lower": lambda df, p: bollinger(df[p.get("source", "Close")], p["period"], p.get("std", 2.0), p.get("ddof", 1))[2],
    "atr": lambda df, p: atr(df, p["period"]),
    "slope": lambda df, p: slope(df[p.get("source", "Close")], p["period"]),
    "vwap": lambda df, p: vwap(df),
}


def compute_indicators(df, indicator_configs):
    """Compute all indicators declared by a strategy.

    Args:
        df: OHLCV DataFrame
        indicator_configs: dict from Strategy.indicators()

    Returns:
        dict of {name: pd.Series}
    """
    results = {}
    for name, (ind_type, params) in indicator_configs.items():
        if ind_type not in INDICATOR_REGISTRY:
            raise ValueError(
                f"Unknown indicator type '{ind_type}'. "
                f"Available: {list(INDICATOR_REGISTRY.keys())}"
            )
        results[name] = INDICATOR_REGISTRY[ind_type](df, params)
    return results
