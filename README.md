[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/saikodi/AutoForge?style=social)](https://github.com/saikodi/AutoForge)

# AutoForge

**Forge strategies through human-AI collaboration.**

<p align="center">
  <img src="docs/images/00_hero.png" alt="AutoForge — You bring the edge, we test it, you get the answer" width="100%">
</p>

AutoForge is an open-source workbench where you describe your edge in plain English, and an AI partner helps you code it, stress-test it, optimize it, and tell you if it's real.

Inspired by [Karpathy's AutoResearch](https://github.com/karpathy/autoresearch), but for a fundamentally different domain. AutoResearch runs quick ML experiments (5-minute wallclock, gradient descent, loss curves). AutoForge is about **rule-based systems** — deterministic strategies with discrete parameters, optimized through exhaustive search across hundreds or thousands of combinations.

> *If you've got the edge, we've got the power to make you successful.*

---

## Table of Contents

- [Philosophy](#philosophy)
- [How It Works — A Real Case Study](#how-it-works--a-real-case-study)
- [What It Looks Like](#what-it-looks-like)
- [How It's Different](#how-its-different)
- [Quick Start](#quick-start)
- [Core Architecture](#core-architecture)
- [Beyond Trading](#beyond-trading)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)

---

## Philosophy

- **You bring the edge.** AutoForge doesn't give you a strategy. You bring your market intuition, your years of screen time, your observations about how price moves. AutoForge helps you formalize it, test it rigorously, and optimize it.

- **AI as research partner, not black box.** The AI interviews you, asks clarifying questions, suggests conditions you haven't considered, and surfaces blind spots. Then it does the grunt work — coding, backtesting, sweeping thousands of parameter combinations. This is **human-AI collaboration**, not autonomous AI — the human's domain expertise drives every decision.

- **Prove it or kill it.** Every idea gets stress-tested across historical data. If the edge isn't there, AutoForge will show you. Better to find out in backtest than with real money.

- **The method, not the alpha.** AutoForge ships the forge — you bring your own metal. No proprietary strategies included. Only toy examples (SMA crossover, basic RSI) to demonstrate the workflow.

---

## How It Works — A Real Case Study

AutoForge was used to develop a real NQ futures strategy through **200+ experiments across 8 phases**. The strategy details are intentionally omitted — this is about the **process**.

### The journey: from intuition to validated strategy

It started with a multi-hour interview. The AI asked questions — *"What exactly do you see before the move starts?"*, *"What market conditions make it fail?"*, *"How do you know when to get out?"* — until the trader's years of observation became a precise, testable specification.

Then the real work began:

<p align="center">
  <img src="docs/images/01_quality_funnel.png" alt="Quality Funnel — fewer trades, sharper edge" width="100%">
</p>

Every phase improved signal quality. **60 trades/day with a paper-thin edge became 4.5 trades/day with a Sharpe above 4.** Filters were tested individually and in combinations. Dead ends were caught in hours — trailing stops that hurt performance, a filter that produced zero trades, a signal method with no edge. Each one would have consumed weeks of manual research.

The final output: **one strategy, three risk profiles** — the trader chooses the tradeoff between risk and reward.

<p align="center">
  <img src="docs/images/04_three_profiles.png" alt="Three Risk Profiles" width="100%">
</p>

Validated across **2.5 years of market data** (430 trading days, 1,000+ trades). 86% profitable months. Edge held across market regimes.

**[Read Case Study #1 →](docs/case-study.md)** — 200+ experiments forging a strategy from scratch.

**[Read Case Study #2 →](docs/case-study-mr.md)** — 3,500+ combinations proving a mean reversion edge is real, not an artifact.

---

## What It Looks Like

<p align="center">
  <img src="docs/images/08_terminal.png" alt="AutoForge terminal output" width="100%">
</p>

---

## How It's Different

**vs. Backtrader / FreqTrade / Zipline** — These are backtest engines. You still write the strategy, pick the parameters, and hope. AutoForge is the layer above: the AI writes the strategy with you, sweeps the parameters exhaustively, and tells you what actually works.

**vs. LLMAlpha / autonomous AI trading** — Those systems run fully autonomously. AutoForge keeps the human in the loop — your domain expertise drives the process. The AI amplifies your judgment, it doesn't replace it. The interview phase, the discovery of filters you hadn't considered, the collaborative refinement — that's where the real value is.

**vs. AutoResearch** — Same inspiration, different domain entirely.

| | AutoResearch | AutoForge |
|--|-------------|-----------|
| Domain | ML / neural nets | Rule-based systems |
| Optimization | Gradient descent | Combinatorial parameter sweep |
| Experiment time | 5-minute wallclock | Hundreds of runs, find the best |
| AI role | Autonomous overnight | Collaborative — interviews, discovers, optimizes |
| Edge source | Architecture search | Human domain expertise + AI-assisted discovery |
| Key output | Lower val_bpb | Validated strategy with optimized parameters |

---

## Quick Start

### Prerequisites

- Python 3.10+
- OS: Windows, macOS, or Linux
- Dependencies: numpy, pandas (installed automatically)
- Optional: [hive-mcp](https://github.com/saikodi/hive-compute-mcp) for distributed parameter sweeps

### 1. Install

```bash
git clone https://github.com/saikodi/AutoForge.git
cd AutoForge
pip install -e .
```

### 2. Bring your data

Place your OHLCV CSV files in `data/`. Expected columns: `DateTime, Open, High, Low, Close, Volume`.

```
data/
  NQ_21range.csv
  ES_5min.csv
```

### 3. Talk to the AI

Open `program.md` — it contains the instructions that guide the AI through the collaboration loop. Point your AI agent (Claude, etc.) at this project and start describing your strategy.

### 4. Or run directly

```python
from autoforge import Strategy, backtest, evaluate, optimize

class MyStrategy(Strategy):
    params = {'fast': 10, 'slow': 30}

    def indicators(self):
        return {
            'sma_fast': ('sma', {'period': self.fast, 'source': 'Close'}),
            'sma_slow': ('sma', {'period': self.slow, 'source': 'Close'}),
        }

    def on_bar(self, ctx):
        if ctx.ind['sma_fast'] > ctx.ind['sma_slow'] and ctx.position <= 0:
            ctx.buy()
        elif ctx.ind['sma_fast'] < ctx.ind['sma_slow'] and ctx.position >= 0:
            ctx.sell()

# Backtest
data = prepare.load_csv('data/NQ.csv')
result = backtest.run(MyStrategy(), data, point_value=20.0, commission=3.80)
evaluate.report(result)

# Optimize
best = optimize.sweep(
    MyStrategy,
    data,
    param_grid={'fast': range(5, 20), 'slow': range(20, 60)},
    point_value=20.0,
    workers=6,
)
```

### 5. Scale with hive-mcp

For large parameter sweeps (thousands of combinations), AutoForge integrates with [hive-mcp](https://github.com/saikodi/hive-compute-mcp) to distribute work across idle machines on your network.

```python
results = optimize.sweep(
    MyStrategy,
    data,
    param_grid={'fast': range(5, 50), 'slow': range(20, 100), 'stop': range(10, 50)},
    backend='hive',  # distribute across LAN
)
```

---

## Core Architecture

AutoForge is intentionally minimal — a few files, not a framework.

```
autoforge/
  strategy.py    # Strategy base class — your strategies extend this
  backtest.py    # Runs a strategy against data, produces trades
  prepare.py     # Loads CSV data, computes indicators
  evaluate.py    # Metrics: Sharpe, win rate, profit factor, drawdown
  optimize.py    # Parameter sweep — local multiprocessing or hive-mcp
program.md       # AI agent instructions — the collaboration methodology
examples/        # Toy strategies (SMA crossover, RSI, S5 reversion)
docs/            # Case study with full walkthrough
```

### Strategy Base Class

```python
class Strategy(ABC):
    params = {}                    # Parameter defaults — optimizer overrides these

    def indicators(self):          # Declare what indicators you need
        return {}

    def on_bar(self, ctx):         # Called for each bar — read data, submit orders
        pass
```

### Fill Logic

Realistic fill simulation that matches how real platforms work:

- **Market orders** fill at the next bar's Open (you decide on bar N, fill on bar N+1)
- **Limit orders** fill at your price if the next bar's range includes it
- Configurable slippage and commission

### Indicators

Built-in: SMA, EMA, RSI, Bollinger Bands (sample std, ddof=1), ATR, VWAP, Slope.
Extensible — add your own in `prepare.py`.

---

## Origin Story

This project grew out of real trading research. The author spent years developing futures strategies, hit the limits of manual parameter tuning, and built AutoForge to systematize the process. When single-machine sweeps weren't enough, [hive-mcp](https://github.com/saikodi/hive-compute-mcp) was born to distribute compute across idle LAN machines.

Both are now open-source: AutoForge for the methodology, hive-mcp for the compute.

---

## Beyond Trading

While trading is the proof case, AutoForge's pattern — **AI interviews human expert, codes rule-based logic, exhaustively optimizes parameters** — applies to any domain with tunable rule-based systems:

- Alert threshold tuning
- Scoring/ranking systems
- Manufacturing process rules
- Decision trees with configurable cutoffs

The forge doesn't care what you're forging.

---

## Disclaimer

AutoForge is a research and educational tool. It does not provide financial advice. Trading futures and other financial instruments involves substantial risk of loss and is not suitable for all investors. Past performance — including any results shown in this repository — is not indicative of future results. Always do your own research and consult with a qualified financial advisor before trading with real money. Use AutoForge at your own risk.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)
