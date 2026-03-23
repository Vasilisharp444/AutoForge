"""Example: S5 — Mean Reversion to Moving Average

A demonstration of how AutoForge was used to develop a real futures strategy
through 200+ experiments across 8 phases (see docs/case-study.md).

This example shows the FRAMEWORK and METHODOLOGY — not the actual strategy.
The signal detection, filters, and parameters here are simplified stand-ins.
The real value is in the process: baseline → filter discovery → parameter
sweep → exit refinement → validation → risk management.

Usage:
    # Single backtest with default parameters
    python examples/s5_reversion.py --data data/NQ.csv

    # Parameter sweep
    python examples/s5_reversion.py --data data/NQ.csv --optimize

    # Sweep a specific phase (filter combos, exit tuning, etc.)
    python examples/s5_reversion.py --data data/NQ.csv --optimize --phase filters
"""

import sys
import argparse
sys.path.insert(0, ".")

from autoforge.strategy import Strategy
from autoforge import backtest, prepare, evaluate, optimize


class S5Reversion(Strategy):
    """Mean reversion to a moving average with context filters.

    Core idea: when price extends too far from its average, enter a
    reversion trade back toward the mean — but only when context
    conditions confirm the setup.

    This is a SIMPLIFIED DEMO. The actual S5 strategy that produced
    the case study results uses proprietary signal detection and filters.
    """

    params = {
        # Signal detection
        "ma_period": 55,
        "min_distance": 15,

        # Risk management
        "stop_points": 25,
        "max_bars": 80,
        "target_buffer": 0,

        # Filters (toggle on/off)
        "use_trend_filter": True,
        "use_extension_filter": True,

        # Filter thresholds
        "trend_period": 21,
        "extension_threshold": 10,

        # Drawdown control (Phase 7)
        "daily_loss_limit": 0,       # 0 = disabled
        "cooldown_bars": 0,          # bars to skip after a stop-out
    }

    def indicators(self):
        return {
            "ma": ("ema", {"period": self.ma_period, "source": "Close"}),
            "ma_slope": ("slope", {"period": 5, "source": "Close"}),
            "rsi": ("rsi", {"period": 14, "source": "Close"}),
            "atr": ("atr", {"period": 14}),
            "trend_ma": ("sma", {"period": self.trend_period, "source": "Close"}),
        }

    def on_bar(self, ctx):
        ma = ctx.ind["ma"]
        trend_ma = ctx.ind["trend_ma"]
        atr_val = ctx.ind["atr"]
        close = ctx.bar["Close"]

        # Distance from moving average (in points)
        distance = abs(close - ma)

        # --- ENTRY LOGIC ---
        if ctx.position == 0 and distance >= self.min_distance:
            # Determine direction
            if close < ma:
                # Price below MA — potential long reversion
                if self._check_filters(ctx, direction="long"):
                    ctx.buy()
            elif close > ma:
                # Price above MA — potential short reversion
                if self._check_filters(ctx, direction="short"):
                    ctx.short()

        # --- EXIT LOGIC ---
        elif ctx.position == 1:  # Long
            target = ma - self.target_buffer
            if close >= target or ctx.bars_in_trade >= self.max_bars:
                ctx.sell()
            elif close <= ctx.entry_price - self.stop_points:
                ctx.sell()

        elif ctx.position == -1:  # Short
            target = ma + self.target_buffer
            if close <= target or ctx.bars_in_trade >= self.max_bars:
                ctx.cover()
            elif close >= ctx.entry_price + self.stop_points:
                ctx.cover()

    def _check_filters(self, ctx, direction):
        """Apply context filters. Returns True if setup passes."""
        if self.use_trend_filter:
            trend_ma = ctx.ind["trend_ma"]
            ma = ctx.ind["ma"]
            # Check trend alignment (simplified)
            if direction == "long" and trend_ma > ma:
                return False
            if direction == "short" and trend_ma < ma:
                return False

        if self.use_extension_filter:
            atr_val = ctx.ind["atr"]
            close = ctx.bar["Close"]
            ma = ctx.ind["ma"]
            # Check if price is overextended relative to ATR
            extension = abs(close - ma) / atr_val if atr_val > 0 else 0
            if extension < self.extension_threshold / 10:
                return False

        return True


# ---------------------------------------------------------------------------
# Phase-based optimization (mirrors the case study)
# ---------------------------------------------------------------------------

PHASE_GRIDS = {
    "baseline": {
        # Phase 1: test the raw concept with no filters
        "min_distance": [10, 15, 20, 25, 30],
        "stop_points": [15, 20, 25, 30],
        "use_trend_filter": [False],
        "use_extension_filter": [False],
    },
    "filters": {
        # Phase 2: test individual and combined filters
        "min_distance": [15],
        "stop_points": [25],
        "use_trend_filter": [True, False],
        "use_extension_filter": [True, False],
        "trend_period": [10, 14, 21, 30],
        "extension_threshold": [5, 8, 10, 12, 15],
    },
    "params": {
        # Phase 3: sweep core parameters with best filters locked in
        "min_distance": [10, 12, 15, 18, 20, 25],
        "stop_points": [15, 18, 20, 25, 30],
        "extension_threshold": [5, 8, 10, 12, 14],
        "max_bars": [50, 80, 100],
        "target_buffer": [0, 2, 3, 5],
    },
    "exits": {
        # Phase 4: refine exit with best params locked in
        "stop_points": [15, 18, 20, 22, 25, 28, 30],
        "max_bars": [30, 50, 80, 100, 120],
        "target_buffer": [0, 1, 2, 3, 5],
    },
    "risk": {
        # Phase 7: drawdown control
        "extension_threshold": [10, 12, 14, 15],
        "cooldown_bars": [0, 5, 10, 20],
        "daily_loss_limit": [0, 500, 750, 1000],
    },
}


def main():
    parser = argparse.ArgumentParser(description="S5 Reversion — AutoForge case study example")
    parser.add_argument("--data", required=True, help="Path to OHLCV CSV")
    parser.add_argument("--point-value", type=float, default=20.0,
                        help="Point value (default: 20.0 for NQ)")
    parser.add_argument("--commission", type=float, default=3.80,
                        help="Round-trip commission (default: 3.80)")
    parser.add_argument("--optimize", action="store_true", help="Run parameter sweep")
    parser.add_argument("--phase", choices=PHASE_GRIDS.keys(), default="params",
                        help="Which optimization phase to run")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    data = prepare.load_csv(args.data)
    print(f"Loaded {len(data):,} bars from {args.data}")

    if args.optimize:
        grid = PHASE_GRIDS[args.phase]
        combos = 1
        for v in grid.values():
            combos *= len(v)
        print(f"\n--- Phase: {args.phase} ({combos:,} combinations) ---")

        results = optimize.sweep(
            S5Reversion,
            data,
            param_grid=grid,
            point_value=args.point_value,
            commission=args.commission,
            workers=args.workers,
        )
        optimize.top_n(results, n=10)
    else:
        print("\n--- Single Backtest (default Config B+ params) ---")
        strategy = S5Reversion()
        result = backtest.run(strategy, data, args.point_value, args.commission)
        evaluate.report(result)


if __name__ == "__main__":
    main()
