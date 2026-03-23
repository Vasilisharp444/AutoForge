"""Backtest engine — runs a strategy against data and produces trades."""

import pandas as pd
from autoforge.strategy import Context
from autoforge.prepare import compute_indicators


def _try_fill(order, bar, slippage=0.0):
    """Attempt to fill an order on the given bar.

    Market orders fill at bar Open +/- slippage.
    Limit orders fill at limit price if bar range includes it.

    Returns fill price or None if not filled.
    """
    direction, order_type, price = order

    if order_type == "market":
        if direction in ("buy", "cover"):
            return bar["Open"] + slippage
        else:
            return bar["Open"] - slippage

    elif order_type == "limit":
        if price is None:
            raise ValueError("Limit order requires a price")
        if bar["Low"] <= price <= bar["High"]:
            return price

    return None


def run(strategy, data, point_value=1.0, commission=0.0, slippage=0.0):
    """Run a backtest.

    Args:
        strategy: Strategy instance
        data: OHLCV DataFrame
        point_value: Dollar value per point (e.g., 20.0 for NQ, 2.0 for MNQ)
        commission: Round-trip commission in dollars
        slippage: Points of slippage for market orders

    Returns:
        dict with 'trades' (list of trade dicts) and 'equity' (list of running P&L)
    """
    # Compute indicators
    ind_configs = strategy.indicators()
    indicators = compute_indicators(data, ind_configs)
    warmup = strategy.get_warmup()

    ctx = Context()
    trades = []
    equity = []
    running_pnl = 0.0

    position = 0          # 1=long, -1=short, 0=flat
    entry_price = 0.0
    entry_bar = 0
    pending_orders = []

    for i in range(len(data)):
        bar = data.iloc[i]

        # Fill pending orders from previous bar's signals
        if i > 0 and pending_orders:
            for order in pending_orders:
                fill_price = _try_fill(order, bar, slippage)
                if fill_price is None:
                    continue

                direction = order[0]

                # Close existing position if reversing
                if direction == "buy" and position == -1:
                    pnl = (entry_price - fill_price) * point_value - commission
                    trades.append({
                        "entry_bar": entry_bar,
                        "exit_bar": i,
                        "direction": "short",
                        "entry_price": entry_price,
                        "exit_price": fill_price,
                        "pnl": pnl,
                        "bars_held": i - entry_bar,
                        "entry_time": data.iloc[entry_bar]["DateTime"],
                        "exit_time": bar["DateTime"],
                    })
                    running_pnl += pnl
                    position = 0

                elif direction == "sell" and position == 1:
                    pnl = (fill_price - entry_price) * point_value - commission
                    trades.append({
                        "entry_bar": entry_bar,
                        "exit_bar": i,
                        "direction": "long",
                        "entry_price": entry_price,
                        "exit_price": fill_price,
                        "pnl": pnl,
                        "bars_held": i - entry_bar,
                        "entry_time": data.iloc[entry_bar]["DateTime"],
                        "exit_time": bar["DateTime"],
                    })
                    running_pnl += pnl
                    position = 0

                elif direction == "short" and position == 1:
                    pnl = (fill_price - entry_price) * point_value - commission
                    trades.append({
                        "entry_bar": entry_bar,
                        "exit_bar": i,
                        "direction": "long",
                        "entry_price": entry_price,
                        "exit_price": fill_price,
                        "pnl": pnl,
                        "bars_held": i - entry_bar,
                        "entry_time": data.iloc[entry_bar]["DateTime"],
                        "exit_time": bar["DateTime"],
                    })
                    running_pnl += pnl
                    position = 0

                elif direction == "cover" and position == -1:
                    pnl = (entry_price - fill_price) * point_value - commission
                    trades.append({
                        "entry_bar": entry_bar,
                        "exit_bar": i,
                        "direction": "short",
                        "entry_price": entry_price,
                        "exit_price": fill_price,
                        "pnl": pnl,
                        "bars_held": i - entry_bar,
                        "entry_time": data.iloc[entry_bar]["DateTime"],
                        "exit_time": bar["DateTime"],
                    })
                    running_pnl += pnl
                    position = 0

                # Open new position
                if direction == "buy" and position == 0:
                    position = 1
                    entry_price = fill_price
                    entry_bar = i
                elif direction == "short" and position == 0:
                    position = -1
                    entry_price = fill_price
                    entry_bar = i

            pending_orders = []

        equity.append(running_pnl)

        # Skip warm-up period for signal generation
        if i < warmup:
            continue

        # Update context
        ctx.bar = {
            "Open": bar["Open"],
            "High": bar["High"],
            "Low": bar["Low"],
            "Close": bar["Close"],
            "Volume": bar.get("Volume", 0),
            "DateTime": bar["DateTime"],
        }
        ctx.ind = {name: series.iloc[i] for name, series in indicators.items()}
        ctx.position = position
        ctx.entry_price = entry_price
        ctx.bars_in_trade = (i - entry_bar) if position != 0 else 0
        ctx.bar_index = i
        ctx._pending_orders = []

        # Call strategy
        strategy.on_bar(ctx)

        # Collect orders for next bar
        pending_orders = list(ctx._pending_orders)

    return {"trades": trades, "equity": equity}
