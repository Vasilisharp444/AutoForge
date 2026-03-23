"""Parameter sweep — local multiprocessing or hive-mcp distributed."""

import itertools
from multiprocessing import Pool
from autoforge.backtest import run
from autoforge.evaluate import metrics
from autoforge.prepare import load_csv


def _run_one(args):
    """Run a single parameter combination. Designed for multiprocessing."""
    strategy_class, data_path, param_dict, point_value, commission, slippage = args
    data = load_csv(data_path)
    strategy = strategy_class(**param_dict)
    result = run(strategy, data, point_value, commission, slippage)
    m = metrics(result["trades"])
    return {**param_dict, **m}


def sweep(strategy_class, data, param_grid, point_value=1.0, commission=0.0,
          slippage=0.0, workers=None, sort_by="net_pnl", backend="local",
          data_path=None):
    """Sweep parameter combinations and return sorted results.

    Args:
        strategy_class: Strategy subclass (not instance)
        data: OHLCV DataFrame (used for local backend)
        param_grid: dict of {param_name: [values]}
        point_value: dollar value per point
        commission: round-trip commission
        slippage: points of slippage for market orders
        workers: number of parallel workers (default: CPU count)
        sort_by: metric to sort results by
        backend: 'local' for multiprocessing, 'hive' for hive-mcp
        data_path: path to CSV (required for multiprocessing/hive backends)

    Returns:
        list of dicts, sorted by sort_by descending
    """
    param_names = list(param_grid.keys())
    combos = list(itertools.product(*param_grid.values()))
    total = len(combos)

    print(f"AutoForge: sweeping {total:,} parameter combinations...")

    if backend == "hive":
        return _sweep_hive(strategy_class, data_path, param_names, combos,
                           point_value, commission, slippage, sort_by)

    if backend == "local" and data_path and workers != 1:
        # Multiprocessing — each worker loads data independently
        args_list = [
            (strategy_class, data_path,
             dict(zip(param_names, combo)),
             point_value, commission, slippage)
            for combo in combos
        ]
        with Pool(workers) as pool:
            results = pool.map(_run_one, args_list)
    else:
        # Single-process — use data directly
        results = []
        for idx, combo in enumerate(combos):
            params = dict(zip(param_names, combo))
            strategy = strategy_class(**params)
            result = run(strategy, data, point_value, commission, slippage)
            m = metrics(result["trades"])
            results.append({**params, **m})
            if (idx + 1) % 100 == 0:
                print(f"  ... {idx + 1}/{total} done")

    results.sort(key=lambda x: x.get(sort_by, 0), reverse=True)

    print(f"AutoForge: sweep complete. Best {sort_by}: {results[0][sort_by]}")
    return results


def _sweep_hive(strategy_class, data_path, param_names, combos,
                point_value, commission, slippage, sort_by):
    """Distribute sweep across hive-mcp workers.

    Generates code strings (not pickled objects) so workers only need
    autoforge installed — no version mismatch issues.
    """
    try:
        # hive-mcp integration — import at runtime so it's optional
        import json

        tasks = []
        for combo in combos:
            params = dict(zip(param_names, combo))
            # Generate a self-contained code string for the worker
            code = _generate_task_code(strategy_class, data_path, params,
                                       point_value, commission, slippage)
            tasks.append({"code": code, "params": params})

        print(f"Generated {len(tasks)} hive tasks. Submit via hive-mcp.")
        print("Example task code:\n")
        print(tasks[0]["code"][:500] + "...")
        return tasks

    except Exception as e:
        print(f"Hive backend error: {e}. Falling back to local.")
        raise


def _generate_task_code(strategy_class, data_path, params,
                         point_value, commission, slippage):
    """Generate self-contained Python code for a hive worker."""
    params_repr = repr(params)
    # Get the strategy class source module and name
    module = strategy_class.__module__
    class_name = strategy_class.__name__

    return f"""
import sys
sys.path.insert(0, '.')
from {module} import {class_name}
from autoforge.prepare import load_csv
from autoforge.backtest import run
from autoforge.evaluate import metrics

data = load_csv({data_path!r})
strategy = {class_name}(**{params_repr})
result = run(strategy, data, point_value={point_value}, commission={commission}, slippage={slippage})
m = metrics(result['trades'])
result_dict = {{**{params_repr}, **m}}
print(result_dict)
"""


def top_n(results, n=10, sort_by="net_pnl"):
    """Print top N parameter combinations."""
    sorted_results = sorted(results, key=lambda x: x.get(sort_by, 0), reverse=True)

    if not sorted_results:
        print("No results.")
        return

    # Get param names (keys that aren't metrics)
    metric_keys = {
        "net_pnl", "trades", "win_rate", "profit_factor", "sharpe",
        "max_drawdown", "avg_win", "avg_loss", "avg_bars_held",
        "long_pnl", "short_pnl", "profitable_days_pct",
    }
    param_keys = [k for k in sorted_results[0] if k not in metric_keys]

    print(f"\nTop {n} by {sort_by}:")
    print("-" * 80)
    header = "  ".join(f"{k:>10}" for k in param_keys)
    header += "  " + "  ".join(f"{k:>12}" for k in ["net_pnl", "sharpe", "win_rate", "trades", "max_dd"])
    print(header)
    print("-" * 80)

    for r in sorted_results[:n]:
        row = "  ".join(f"{r[k]:>10}" for k in param_keys)
        row += f"  ${r['net_pnl']:>11,.2f}"
        row += f"  {r['sharpe']:>12}"
        row += f"  {r['win_rate']:>11}%"
        row += f"  {r['trades']:>12,}"
        row += f"  ${r['max_drawdown']:>10,.2f}"
        print(row)

    print("-" * 80)
