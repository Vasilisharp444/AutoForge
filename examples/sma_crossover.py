"""Example: Simple Moving Average Crossover

A classic toy strategy to demonstrate AutoForge's workflow.
This is NOT a profitable strategy — it's here to show the framework.

Usage:
    python examples/sma_crossover.py --data data/your_data.csv
"""

import sys
import argparse
sys.path.insert(0, ".")

from autoforge.strategy import Strategy
from autoforge import backtest, prepare, evaluate, optimize


class SMACrossover(Strategy):
    """Buy when fast SMA crosses above slow SMA, sell when it crosses below."""

    params = {
        "fast_period": 10,
        "slow_period": 30,
    }

    def indicators(self):
        return {
            "sma_fast": ("sma", {"period": self.fast_period, "source": "Close"}),
            "sma_slow": ("sma", {"period": self.slow_period, "source": "Close"}),
        }

    def on_bar(self, ctx):
        fast = ctx.ind["sma_fast"]
        slow = ctx.ind["sma_slow"]

        if fast > slow and ctx.position <= 0:
            ctx.buy()
        elif fast < slow and ctx.position > 0:
            ctx.sell()


def main():
    parser = argparse.ArgumentParser(description="SMA Crossover — AutoForge example")
    parser.add_argument("--data", required=True, help="Path to OHLCV CSV")
    parser.add_argument("--point-value", type=float, default=1.0)
    parser.add_argument("--commission", type=float, default=0.0)
    parser.add_argument("--optimize", action="store_true", help="Run parameter sweep")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    data = prepare.load_csv(args.data)
    print(f"Loaded {len(data):,} bars from {args.data}")

    if args.optimize:
        print("\n--- Parameter Sweep ---")
        results = optimize.sweep(
            SMACrossover,
            data,
            param_grid={
                "fast_period": range(5, 25),
                "slow_period": range(20, 60),
            },
            point_value=args.point_value,
            commission=args.commission,
            workers=args.workers,
        )
        optimize.top_n(results, n=10)
    else:
        print("\n--- Single Backtest ---")
        strategy = SMACrossover()
        result = backtest.run(strategy, data, args.point_value, args.commission)
        evaluate.report(result)


if __name__ == "__main__":
    main()
