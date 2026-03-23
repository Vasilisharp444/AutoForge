# AutoForge Launch Posts

---

## 1. Hacker News (Show HN)

**Title:** Show HN: AutoForge – Forge trading strategies through human-AI collaboration (inspired by Karpathy's AutoResearch)

**Body:**

I spent 10+ years trading NQ futures and observing patterns. Turning those observations into validated, optimized strategies used to take months of manual work. So I built AutoForge.

The idea: you describe your edge in plain English, an AI partner interviews you until the spec is tight, codes the strategy, sweeps thousands of parameter combinations, and tells you if the edge is real — or if you're fooling yourself.

Inspired by Karpathy's AutoResearch, but for a fundamentally different domain. AutoResearch runs 5-minute ML experiments with gradient descent. AutoForge is about rule-based systems — deterministic strategies with discrete parameters, optimized through exhaustive combinatorial search.

Key difference from autonomous AI systems: AutoForge keeps the human in the loop. The AI interviews you, suggests conditions you haven't considered, and does the grunt work. But you make every decision. Your domain expertise drives the process.

Two real case studies in the repo (strategy details sanitized):

- Case Study #1: 200+ experiments across 8 phases. Went from 60 trades/day with a paper-thin edge to 4.5 trades/day with a Sharpe above 4.
- Case Study #2: 3,500+ parameter combinations swept. 97% profitable. Random entries with the same mechanics lost catastrophically (-$152K to -$2.1M). The signals are real.

The framework is minimal by design — 6 Python files, not a framework. No proprietary strategies included.

When single-machine sweeps weren't enough, I built hive-mcp (also open-source) to distribute parameter sweeps across idle LAN machines.

GitHub: https://github.com/saikodi/AutoForge

While trading is the proof case, the pattern — AI interviews domain expert, codes rule-based logic, exhaustively optimizes parameters — applies to any domain with tunable rule-based systems.

---

## 2. Reddit: r/algotrading

**Title:** I built an AI research partner that ran 3,500+ parameter combinations to validate my futures strategy. Open-sourcing the framework.

**Body:**

After 10+ years trading NQ futures, I had a collection of market observations I'd never formalized into code. I built AutoForge to change that.

**What it does:** You describe your strategy idea to an AI. It interviews you — asks hard questions, pushes back on vague answers, suggests conditions you haven't considered. Then it codes the strategy, sweeps thousands of parameter combinations, and validates the edge with ablation tests, random baselines, and stop sensitivity sweeps.

**What it doesn't do:** It doesn't give you a strategy. You bring the edge. AutoForge tells you if it's real.

**Two real case studies in the repo (no proprietary details revealed):**

**Case Study #1 — Forging from scratch:**
- Started with a market intuition and a multi-hour AI interview
- 200+ experiments across 8 phases
- 5 signal detection methods tested, 8 filters evaluated individually and in combinations
- 1,400+ parameter combinations swept
- Dead ends caught in hours (trailing stops hurt performance, one filter produced zero trades, one signal method had no edge)
- Final result: three risk profiles — the trader picks the tradeoff

**Case Study #2 — Proving the edge is real:**
- 3,500+ parameter combinations tested
- 97% of combinations were profitable (broad plateau, not a fragile peak)
- Every stop level tested (18 levels) was profitable
- Random entries with the same stop/target mechanics: -$152K to -$2.1M across 25 trials
- Ablation tests confirmed each signal component contributes independently
- Combined with an uncorrelated strategy: 32% drawdown reduction

**The framework:**
- 6 Python files, minimal dependencies (numpy + pandas)
- Strategy base class with `on_bar(ctx)` — if you've used NinjaTrader's OnBarUpdate, same idea
- Realistic fill logic (market orders at next bar Open, limit orders at price if touched)
- Local multiprocessing for sweeps, optional distributed compute via hive-mcp
- No proprietary strategies included — only toy examples (SMA crossover, basic RSI)

Inspired by Karpathy's AutoResearch but for rule-based systems, not ML.

GitHub: https://github.com/saikodi/AutoForge

Happy to answer questions about the methodology.

---

## 3. Reddit: r/LocalLLaMA

**Title:** Used Claude as an AI research partner to run 200+ trading strategy experiments — open-sourcing the framework

**Body:**

Built something I think this community would find interesting — not because it's about trading specifically, but because of the human-AI collaboration pattern.

**The setup:** I have 10+ years of trading observations that I'd never formalized. I built AutoForge — a framework where:

1. You describe your idea in plain English
2. The AI **interviews you** — asks clarifying questions, challenges vague answers, suggests parameters you haven't considered
3. The AI codes the strategy
4. Sweeps hundreds/thousands of parameter combinations
5. Validates rigorously — ablation tests, random baselines, sensitivity sweeps
6. Reports honestly — if there's no edge, it says so

**Why this is different from autonomous AI:**

Most AI-for-X projects are fully autonomous — fire and forget. AutoForge keeps the human in the loop because **domain expertise matters**. The AI asked questions I hadn't considered (session filters, asymmetric parameters for long vs short). I caught things the AI missed (a filter that contradicted the strategy's thesis). Neither of us could have done it alone.

**The interview phase is the secret sauce.** A multi-hour back-and-forth before any code is written. The AI pushes: "What exactly do you see before the move starts?" "What market conditions make it fail?" "How do you know when to get out?" By the end, vague intuition becomes a precise specification.

**Scale:** One case study ran 3,500+ parameter combinations. 97% were profitable. Random entries with the same mechanics lost catastrophically. The signals are real.

The framework is 6 Python files. Inspired by Karpathy's AutoResearch but for rule-based systems instead of ML.

GitHub: https://github.com/saikodi/AutoForge

The pattern — AI interviews expert, codes rules, exhaustively optimizes — works beyond trading. Anywhere you have tunable rule-based systems.

---

## 4. X/Twitter Thread

**Tweet 1 (hook):**

I spent 10 years watching NQ futures. I had observations I never formalized.

So I built AutoForge — an AI research partner that interviewed me, coded my strategy, swept 3,500+ parameter combinations, and told me if the edge was real.

Open-sourcing it today. 🧵

**Tweet 2 (the problem):**

The problem with manual strategy development:

• You test 5-10 parameter combos by hand
• You pick the one that "looks good"
• You have no idea if it's overfit
• You never test the 1,400 combos you didn't try

AutoForge tests ALL of them.

**Tweet 3 (how it works):**

How it works:

1. You describe your edge in plain English
2. AI interviews you until the spec is tight
3. AI codes the strategy
4. Sweeps thousands of parameter combos
5. Validates: ablation tests, random baselines, stop sensitivity
6. Reports honestly — edge or no edge

**Tweet 4 (case study 1):**

Case Study #1: 200+ experiments

• 5 signal methods tested → 2 kept, 1 had zero edge
• 8 filters → best pair found, 3rd filter was redundant
• Trailing stops tested → they HURT (counterintuitive)
• 60 trades/day → 4.5 trades/day
• Sharpe: 0.05 → 4.13

**Tweet 5 (case study 2):**

Case Study #2: 3,500+ parameter combos

• 97% of combinations profitable
• All 18 stop levels profitable
• Random entries: -$2.1M (25 trials)
• Strategy signals: profitable

The edge is real. Not a fragile peak — a broad plateau.

**Tweet 6 (the insight):**

The key insight: this is NOT autonomous AI.

The AI interviewed me for hours before writing a line of code. It asked questions I hadn't considered. I caught things it missed.

Neither of us could have done it alone. Human-AI collaboration > fully autonomous.

**Tweet 7 (inspiration):**

Inspired by @karpathy's AutoResearch — same philosophy of simplicity (6 files, not a framework), but different domain.

AutoResearch: ML experiments, gradient descent, 5-minute runs
AutoForge: Rule-based systems, combinatorial search, thousands of runs

**Tweet 8 (origin story):**

Origin story:

Built trading strategies → needed more parameter sweeps → single machine too slow → built hive-mcp (distributed compute for AI agents) → now open-sourcing both.

AutoForge: github.com/saikodi/AutoForge
hive-mcp: github.com/saikodi/hive-compute-mcp

**Tweet 9 (CTA):**

AutoForge doesn't give you an edge. You bring the edge. AutoForge stress-tests it, optimizes it, and tells you if it's real.

If you've got the edge, we've got the power to make you successful.

⭐ github.com/saikodi/AutoForge

---

## 5. Reddit: r/futuresTrading

**Title:** Open-sourcing the framework I used to validate my NQ strategies — 3,500+ parameter combinations, ablation tests, random baselines

**Body:**

I've been trading NQ for 10+ years. Last month I built a framework to systematize how I develop and validate strategies. Open-sourcing the framework (not the strategies).

**What AutoForge does:**

You describe your strategy idea to an AI partner. It interviews you, codes it, then exhaustively tests it:

- Sweeps every parameter combination (not 5-10 by hand — hundreds or thousands)
- Tests stop sensitivity (is the edge real at different stop levels, or only at one magic number?)
- Runs random baseline comparison (do the signals matter, or would random entries also work?)
- Ablation tests (does each component contribute, or is one doing all the work?)
- Time-of-day analysis (which hours make money, which lose?)

**Real results from the case studies (strategy details omitted):**

- 97% of parameter combinations were profitable — broad plateau, not a fragile peak
- All 18 stop levels tested were profitable — the edge doesn't depend on getting the exact stop right
- Random entries with the same mechanics lost -$152K to -$2.1M across 25 trials — the signals are real
- Two specific hours consistently lost money — excluding them improved Sharpe without reducing good trades

**What it's NOT:**
- Not a strategy library (no alpha included)
- Not a signal service
- Not an automated trading bot

It's a workbench for people who already have ideas and want to test them rigorously. 21-range bars, any instrument, realistic fills (market orders at next bar Open, limit orders at price if touched).

**The fill logic matters:** Market orders fill at next bar's Open with configurable slippage. Limit orders fill at your price if the bar's range includes it. Matches how NinjaTrader fills on range bars.

GitHub: https://github.com/saikodi/AutoForge

If you've been doing parameter optimization by hand, this might save you months.

---

## 6. Reddit: r/ClaudeAI

**Title:** Built AutoForge with Claude — an AI research partner for developing trading strategies. 200+ experiments, two case studies, open source.

**Body:**

Wanted to share a project that showcases Claude as a genuine research partner, not just a code assistant.

**The concept:** I have 10+ years of trading observations. I used Claude to turn those into validated, optimized strategies. But not in the usual "write me a function" way — Claude conducted multi-hour interviews, pushed back on vague ideas, suggested parameters I hadn't considered, and then did the grunt work of coding, backtesting, and sweeping thousands of parameter combinations.

**What made this work:**

1. **The interview phase** — Claude asked: "What exactly do you see before the move starts?" "What market conditions make it fail?" "How do you know when to get out?" It wouldn't let me be vague. By the end, years of intuition became a precise specification.

2. **Discovery** — Claude suggested 8 different filters I could test. One produced zero trades (wrong calibration for my bar type — caught in minutes, would've taken days to discover manually). Another contradicted the strategy's thesis — removing it actually improved performance. Counterintuitive, but the data was clear.

3. **Scale** — Claude ran 3,500+ parameter combinations, tested 18 stop levels, ran 25 random baseline trials. One case study had 200+ experiments across 8 phases.

4. **Honesty** — When trailing stops hurt performance (counterintuitive for a trader), Claude showed the data and explained why. When a third filter was redundant, Claude flagged it: "Adding complexity without improvement is a red flag."

**The `program.md` approach:** Inspired by Karpathy's AutoResearch. Instead of prompting Claude directly each time, I wrote a `program.md` file that instructs Claude how to interview, discover, optimize, and validate. Claude reads it and follows the methodology. You iterate on `program.md` over time to improve the research process itself.

Open-sourcing the framework (not the strategies): https://github.com/saikodi/AutoForge

Two sanitized case studies in the repo show the full process — every phase, every decision, every dead end.

---

## 7. Elite Trader / NinjaTrader Forums

**Title:** Open-Source Strategy Validation Framework — Exhaustive Parameter Sweeps + Statistical Validation

**Body:**

Sharing an open-source tool I built for systematic strategy validation. Been trading NQ for 10+ years, got tired of testing 5-10 parameter combos by hand and hoping I picked the right one.

**AutoForge** pairs you with an AI that:
- Codes your strategy from a plain-English description
- Sweeps every parameter combination (not 5-10 — hundreds or thousands)
- Tests stop sensitivity across 18+ levels
- Runs random baseline comparisons (do the signals actually add value?)
- Performs ablation tests (does each component contribute?)

**Fill logic matches NinjaTrader:** Market orders fill at next bar's Open. Limit orders fill at price if the bar's range includes it. Configurable slippage and commission. Designed for range bars.

**Why I built it:**
I was manually testing parameters in NinjaTrader's Strategy Analyzer, which works fine for 10-20 combinations. But when you have 6 parameters with 5 values each, that's 15,625 combinations. No one's doing that by hand.

AutoForge sweeps them all on your PC (6 parallel workers) or distributes across multiple machines if you have them.

**What the validation showed (from the case studies):**
- 97% of parameter combos profitable — the edge is a plateau, not a peak
- All 18 stop levels profitable — not dependent on one magic number
- Random entries with same mechanics: massive losses — signals matter
- Trailing stops HURT a mean reversion strategy (counterintuitive but data was clear)

**No strategies included.** Framework only. You bring your ideas, it tests them.

NQ/MNQ focused but works with any OHLCV data. Python 3.10+, numpy, pandas.

https://github.com/saikodi/AutoForge

Happy to discuss the methodology.

---

## 8. Reddit: r/MachineLearning

**Title:** AutoForge: Karpathy's AutoResearch concept applied to rule-based systems — combinatorial optimization instead of gradient descent

**Body:**

Karpathy's AutoResearch is brilliant for ML: agent modifies code, trains for 5 minutes, evaluates val_bpb, keeps or discards, repeats.

I adapted the concept for a completely different domain: **rule-based systems with discrete parameters.** No neural nets, no gradients, no loss curves. Instead: deterministic rules, combinatorial parameter sweeps, and statistical validation.

**Why this is interesting from an optimization perspective:**

The search space is different. ML optimization follows gradients in continuous space. Rule-based optimization is combinatorial — 6 parameters × 5 values each = 15,625 discrete combinations. No gradient to follow. You have to search.

**What makes the AI useful here isn't coding — it's discovery:**

The AI interviewed the domain expert (a trader) and suggested 8 filter conditions to test. One produced zero results (wrong calibration for the data type). One contradicted the strategy's thesis — removing it improved performance. A third filter was redundant (adding it to the best pair didn't change results). These discoveries would take weeks manually.

**Validation methodology:**
- Ablation tests (remove each signal component, measure impact)
- Random baseline comparison (25 trials with same mechanics, all lost catastrophically)
- Stop sensitivity sweep (18 levels, all profitable — broad plateau, not overfit)
- Out-of-sample: 2.5 years, 1,000+ trades, 86% profitable months

**The framework:**
- 6 Python files, ~1,200 lines total
- Strategy base class → backtest engine → parameter sweep (multiprocessing or distributed)
- Inspired by AutoResearch's simplicity philosophy

**Not ML, and that's the point.** Many real-world optimization problems are rule-based with discrete parameters: alert thresholds, scoring systems, manufacturing rules, decision trees. This approach works for all of them.

GitHub: https://github.com/saikodi/AutoForge

---

## 9. Dev.to / Hashnode Blog Post

**Title:** How I Used AI to Run 3,500+ Experiments and Validate a Trading Strategy

**Subtitle:** Building AutoForge — an open-source framework for human-AI collaboration on rule-based optimization

*(Use the case study content from docs/case-study-mr.md as the body, with an intro explaining the project and a CTA at the end linking to the repo)*

---

## Posting Strategy

**Day 1:** Hacker News (Show HN) + Twitter thread
**Day 1-2:** r/algotrading + r/ClaudeAI (highest-relevance communities)
**Day 3:** r/LocalLLaMA + r/MachineLearning
**Day 4:** r/futuresTrading + Elite Trader / NT forums
**Day 5:** Dev.to / Hashnode blog post
**Ongoing:** Respond to every comment, answer questions, be genuinely helpful
