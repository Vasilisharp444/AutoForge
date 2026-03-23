"""Metrics and reporting for backtest results."""

import numpy as np
import pandas as pd


def metrics(trades, point_value=1.0):
    """Compute strategy metrics from a list of trade dicts.

    Args:
        trades: list of trade dicts from backtest.run()
        point_value: for display only (P&L already in dollars)

    Returns:
        dict of metric name -> value
    """
    if not trades:
        return {
            "net_pnl": 0.0, "trades": 0, "win_rate": 0.0,
            "profit_factor": 0.0, "sharpe": 0.0, "max_drawdown": 0.0,
            "avg_win": 0.0, "avg_loss": 0.0, "avg_bars_held": 0.0,
            "long_pnl": 0.0, "short_pnl": 0.0, "profitable_days_pct": 0.0,
        }

    pnls = np.array([t["pnl"] for t in trades])
    winners = pnls[pnls > 0]
    losers = pnls[pnls <= 0]

    net_pnl = pnls.sum()
    gross_win = winners.sum() if len(winners) else 0.0
    gross_loss = abs(losers.sum()) if len(losers) else 0.0

    # Sharpe: annualized daily returns
    daily_pnl = _daily_pnl(trades)
    if len(daily_pnl) > 1 and daily_pnl.std() > 0:
        sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)
    else:
        sharpe = 0.0

    # Max drawdown from cumulative P&L
    cum_pnl = np.cumsum(pnls)
    peak = np.maximum.accumulate(cum_pnl)
    drawdown = peak - cum_pnl
    max_dd = drawdown.max() if len(drawdown) else 0.0

    # Long/short breakdown
    long_pnl = sum(t["pnl"] for t in trades if t["direction"] == "long")
    short_pnl = sum(t["pnl"] for t in trades if t["direction"] == "short")

    # Profitable days
    if len(daily_pnl) > 0:
        profitable_days = (daily_pnl > 0).sum() / len(daily_pnl) * 100
    else:
        profitable_days = 0.0

    return {
        "net_pnl": round(net_pnl, 2),
        "trades": len(trades),
        "win_rate": round(len(winners) / len(trades) * 100, 1),
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf"),
        "sharpe": round(sharpe, 2),
        "max_drawdown": round(max_dd, 2),
        "avg_win": round(winners.mean(), 2) if len(winners) else 0.0,
        "avg_loss": round(losers.mean(), 2) if len(losers) else 0.0,
        "avg_bars_held": round(np.mean([t["bars_held"] for t in trades]), 1),
        "long_pnl": round(long_pnl, 2),
        "short_pnl": round(short_pnl, 2),
        "profitable_days_pct": round(profitable_days, 1),
    }


def _daily_pnl(trades):
    """Aggregate trade P&L by exit date."""
    if not trades:
        return pd.Series(dtype=float)
    df = pd.DataFrame(trades)
    df["exit_date"] = pd.to_datetime(df["exit_time"]).dt.date
    return df.groupby("exit_date")["pnl"].sum()


def report(result, point_value=1.0):
    """Print a formatted report of backtest results."""
    m = metrics(result["trades"], point_value)
    n_days = len(_daily_pnl(result["trades"]))
    daily_avg = m["net_pnl"] / n_days if n_days > 0 else 0

    print("=" * 50)
    print("  AutoForge Backtest Report")
    print("=" * 50)
    print(f"  Net P&L:          ${m['net_pnl']:>12,.2f}")
    print(f"  Daily Avg:        ${daily_avg:>12,.2f}  ({n_days} days)")
    print(f"  Trades:           {m['trades']:>12,}")
    print(f"  Win Rate:         {m['win_rate']:>11}%")
    print(f"  Profit Factor:    {m['profit_factor']:>12}")
    print(f"  Sharpe Ratio:     {m['sharpe']:>12}")
    print(f"  Max Drawdown:     ${m['max_drawdown']:>12,.2f}")
    print(f"  Avg Win:          ${m['avg_win']:>12,.2f}")
    print(f"  Avg Loss:         ${m['avg_loss']:>12,.2f}")
    print(f"  Avg Bars Held:    {m['avg_bars_held']:>12}")
    print("-" * 50)
    print(f"  Long P&L:         ${m['long_pnl']:>12,.2f}")
    print(f"  Short P&L:        ${m['short_pnl']:>12,.2f}")
    print(f"  Profitable Days:  {m['profitable_days_pct']:>11}%")
    print("=" * 50)

    return m
