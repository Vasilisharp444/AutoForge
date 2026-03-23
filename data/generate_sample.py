"""
Generate synthetic NQ 21-range bar OHLCV data for demo/testing purposes.
Produces ~5,000 bars of realistic price action around 18000-19000.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# --- Parameters ---
NUM_BARS = 5000
RANGE_SIZE = 21  # 21-point range bars
MEAN_PRICE = 18500
REVERSION_STRENGTH = 0.002  # pull back toward mean
VOLATILITY = 8.0  # per-bar drift std
VOLUME_LOW, VOLUME_HIGH = 50, 500

# --- Generate price random walk with mean reversion ---
prices = np.zeros(NUM_BARS + 1)
prices[0] = MEAN_PRICE

for i in range(1, NUM_BARS + 1):
    drift = -REVERSION_STRENGTH * (prices[i - 1] - MEAN_PRICE)
    shock = np.random.normal(0, VOLATILITY)
    prices[i] = prices[i - 1] + drift + shock

# --- Build OHLCV from the walk ---
opens = prices[:-1]
closes = prices[1:]

rows = []
for i in range(NUM_BARS):
    o = round(opens[i], 2)
    c = round(closes[i], 2)

    # Range bars: High - Low ≈ 21 points
    mid = (o + c) / 2
    bar_body = abs(o - c)

    # Wicks fill remaining range; at minimum H-L = body
    remaining = max(RANGE_SIZE - bar_body, 0)
    upper_wick = np.random.uniform(0.3, 0.7) * remaining
    lower_wick = remaining - upper_wick

    h = round(max(o, c) + upper_wick, 2)
    l = round(min(o, c) - lower_wick, 2)

    vol = np.random.randint(VOLUME_LOW, VOLUME_HIGH + 1)
    rows.append((o, h, l, c, vol))

# --- Generate timestamps across ~10 trading days (Pacific Time) ---
# NQ futures: Sun 3:00 PM – Fri 4:00 PM PT, with 15-min break 1:00-1:15 PM PT daily
# Simplified: bars spread across 23 trading hours per day

start_date = datetime(2025, 3, 10, 15, 0, 0)  # Monday 3 PM PT session open
bars_per_day = NUM_BARS // 10
timestamps = []
current = start_date

for i in range(NUM_BARS):
    # Skip weekends
    while current.weekday() >= 5:  # Sat=5, Sun=6
        current += timedelta(days=1)
        current = current.replace(hour=15, minute=0, second=0)

    timestamps.append(current)

    # Advance by a random interval (range bars are not equally spaced)
    # Average ~23*60/bars_per_day minutes between bars, with jitter
    avg_gap = (23 * 60) / bars_per_day
    gap_seconds = max(10, np.random.exponential(avg_gap * 60))
    current += timedelta(seconds=gap_seconds)

    # If past end-of-session (next day 2 PM), jump to next session (3 PM)
    if current.hour >= 14 and current.hour < 15:
        current = current.replace(hour=15, minute=0, second=0)

# --- Assemble DataFrame ---
df = pd.DataFrame(rows, columns=["Open", "High", "Low", "Close", "Volume"])
df.insert(0, "DateTime", timestamps)

# Format DateTime nicely
df["DateTime"] = df["DateTime"].dt.strftime("%Y-%m-%d %H:%M:%S") if hasattr(df["DateTime"].iloc[0], "strftime") else df["DateTime"]
df["DateTime"] = pd.to_datetime(df["DateTime"]).dt.strftime("%Y-%m-%d %H:%M:%S")

# --- Save ---
output_path = "C:/enlist/personal/AutoForge/data/sample_NQ.csv"
df.to_csv(output_path, index=False)

# --- Summary ---
print(df.head().to_string(index=False))
print(f"\nTotal rows: {len(df)}")
print(f"Price range: {df['Low'].min():.2f} - {df['High'].max():.2f}")
print(f"Date range: {df['DateTime'].iloc[0]} to {df['DateTime'].iloc[-1]}")
print(f"Saved to: {output_path}")
