"""Example: RSI Mean Reversion

Buy when RSI is oversold, sell when it reverts to the mean.
A toy example to demonstrate indicators and limit orders.

Usage:
    python examples/rsi_mean_reversion.py --data data/your_data.csv
"""

import sys
import argparse
sys.path.insert(0, ".")

from autoforge.strategy import Strategy
from autoforge import backtest, prepare, evaluate, optimize


class RSIMeanReversion(Strategy):
    """Buy at RSI oversold + price below lower Bollinger. Exit at middle BB."""

    params = {
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "bb_period": 20,
        "bb_std": 2.0,
        "max_bars": 30,
    }

    def indicators(self):
        return {
            "rsi": ("rsi", {"period": self.rsi_period, "source": "Close"}),
            "bb_mid": ("bb_mid", {"period": self.bb_period, "std": self.bb_std}),
            "bb_upper": ("bb_upper", {"period": self.bb_period, "std": self.bb_std}),
            "bb_lower": ("bb_lower", {"period": self.bb_period, "std": self.bb_std}),
        }

    def on_bar(self, ctx):
        rsi_val = ctx.ind["rsi"]
        bb_mid = ctx.ind["bb_mid"]
        bb_lower = ctx.ind["bb_lower"]
        bb_upper = ctx.ind["bb_upper"]

        # Entry: RSI oversold and price near lower BB
        if ctx.position == 0:
            if rsi_val < self.rsi_oversold and ctx.bar["Close"] <= bb_lower:
                ctx.buy(order_type="limit", price=bb_lower)
            elif rsi_val > self.rsi_overbought and ctx.bar["Close"] >= bb_upper:
                ctx.short(order_type="limit", price=bb_upper)

        # Exit: price reverts to middle BB or max bars exceeded
        elif ctx.position == 1:
            if ctx.bar["Close"] >= bb_mid or ctx.bars_in_trade >= self.max_bars:
                ctx.sell()
        elif ctx.position == -1:
            if ctx.bar["Close"] <= bb_mid or ctx.bars_in_trade >= self.max_bars:
                ctx.cover()


def main():
    parser = argparse.ArgumentParser(description="RSI Mean Reversion — AutoForge example")
    parser.add_argument("--data", required=True, help="Path to OHLCV CSV")
    parser.add_argument("--point-value", type=float, default=1.0)
    parser.add_argument("--commission", type=float, default=0.0)
    parser.add_argument("--optimize", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    data = prepare.load_csv(args.data)
    print(f"Loaded {len(data):,} bars from {args.data}")

    if args.optimize:
        print("\n--- Parameter Sweep ---")
        results = optimize.sweep(
            RSIMeanReversion,
            data,
            param_grid={
                "rsi_period": [10, 14, 20],
                "rsi_oversold": [25, 30, 35],
                "rsi_overbought": [65, 70, 75],
                "bb_period": [15, 20, 30],
                "bb_std": [1.5, 2.0, 2.5],
                "max_bars": [20, 30, 50],
            },
            point_value=args.point_value,
            commission=args.commission,
            workers=args.workers,
        )
        optimize.top_n(results, n=10)
    else:
        print("\n--- Single Backtest ---")
        strategy = RSIMeanReversion()
        result = backtest.run(strategy, data, args.point_value, args.commission)
        evaluate.report(result)


if __name__ == "__main__":
    main()
