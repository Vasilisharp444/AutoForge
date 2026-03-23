# Case Study: Forging a Futures Strategy from Scratch

**How a human trader and an AI partner turned a market intuition into a validated, optimized strategy — through 200+ experiments across 8 phases.**

This is a real case study from AutoForge's development. The strategy details (indicators, rules, parameters) are intentionally omitted — this is about the **process**, not the alpha.

---

## The Starting Point

The trader had a simple observation:

> *"When price gets stretched too far from its average, it tends to snap back."*

That's it. No code, no parameters, no backtests. Just a market intuition built from years of watching price action on NQ futures (21-range bars, $20/point).

The goal: turn that intuition into a rule-based strategy with quantifiable edge.

---

## Phase 1: Signal Baseline — "Does the core idea even work?"

**Experiments: 10 | Goal: test the raw concept**

The first question wasn't about parameters — it was about **how to detect the snapback**. The AI coded five different signal detection methods and tested each one with minimal filters — just the bare concept.

| Signal | Trades/Day | Win Rate | Profit Factor | Verdict |
|--------|-----------|----------|---------------|---------|
| Method A | 60.3 | 62.9% | 1.01 | Too many trades, paper-thin edge |
| **Method B** | **63.4** | **64.1%** | **1.09** | **Best single signal — KEEP** |
| Method C | 31.2 | 63.7% | 1.03 | Weakest edge |
| Method D | 59.6 | 63.5% | 1.04 | Moderate |
| All combined | 86.4 | 63.2% | 1.06 | Highest raw P&L |

**Key insight:** All five methods showed *some* edge — the core idea was valid. But 60+ trades per day is absurd. The signal fires constantly. We needed filters to separate the high-quality setups from the noise.

**What the AI noticed:** Short trades outperformed long trades across *every* signal method. This asymmetry became important later.

---

## Phase 2: Filter Discovery — "What separates good setups from bad ones?"

**Experiments: 22 | Goal: find filters that improve signal quality**

This is where the AI's breadth showed its value. The trader knew one or two things to look for. The AI suggested **eight different filters** — context conditions that might separate good trades from noise.

### Single filters tested:

| Filter | Trades/Day | Win Rate | Profit Factor | Sharpe | Verdict |
|--------|-----------|----------|---------------|--------|---------|
| Trend alignment | 24.4 | 68.7% | 1.35 | 1.84 | **Strong — KEEP** |
| Slope condition A | 21.1 | 70.8% | 1.40 | 2.36 | **Best single filter** |
| Slope condition B | 57.4 | 70.7% | 1.33 | 2.04 | Good but too many trades |
| **Overextension** | **67.9** | **68.8%** | **1.32** | **1.81** | **Highest raw P&L — KEEP** |
| Exhaustion bars | 51.4 | 68.2% | 1.31 | 1.79 | Keep for combos |
| Climax detection | 0.0 | — | — | — | **Zero trades — DEAD** |
| Exhaustion method B | 54.9 | 67.7% | 1.16 | 0.96 | Too weak |
| Reversal condition | 66.4 | 67.9% | 1.19 | 1.17 | Too weak |

**The climax filter discovery:** One filter — theoretically sound — produced *zero trades* on this bar type. The AI flagged it: the detection threshold was calibrated for time-based bars, not range bars. Rather than waste time adjusting thresholds, we killed it. This is the kind of dead end that can eat weeks of manual research.

### Then: two-filter combinations

The AI systematically tested all promising pairs:

| Combo | Trades/Day | Win Rate | Profit Factor | Sharpe | Verdict |
|-------|-----------|----------|---------------|--------|---------|
| **Trend + Overextension** | **4.5** | **73.8%** | **2.35** | **4.13** | **BEST COMBO** |
| Exhaustion + Overextension | 23.3 | 69.5% | 1.32 | 1.74 | Alternative |
| Exhaustion + Exhaust bars | 6.9 | 71.4% | 1.55 | 3.11 | High quality, fewer trades |
| Trend + Time window | 5.6 | 71.3% | 1.45 | 2.57 | Good but time filter is fragile |
| Exhaust + Trend + Overext | 4.5 | 73.6% | 2.33 | 4.09 | Adding 3rd filter barely helps |

**The diminishing returns lesson:** Adding a third filter to the best pair barely changed anything — same trades, same metrics. The AI flagged this: *"The third filter is redundant. These two conditions already capture the same quality trades. Adding complexity without improvement is a red flag."*

**We went from 60 trades/day to 4.5 trades/day** — and from PF 1.09 to PF 2.35. The filters didn't just reduce quantity, they radically improved quality.

---

## Phase 3: Parameter Grid — "Where are the sweet spots?"

**Experiments: 48 | Goal: map the parameter space**

With the best filter combination locked in, we swept the core numerical parameters:

- **Distance threshold**: How far does price need to stretch? (tested 6 values)
- **Stop loss**: How tight? (tested 5 values)
- **Overextension threshold**: How strict? (tested 4 values)
- **Max hold time**: How long to wait for the target? (tested 3 values)
- **Target offset**: Exit exactly at target or leave a buffer? (tested 4 values)

That's **6 × 5 × 4 × 3 × 4 = 1,440 potential combinations.** The AI first ran a coarse grid to identify the interesting regions, then zoomed in.

### Distance vs. Stop heatmap (simplified):

```
Stop →     15pt    20pt    25pt    30pt
Dist ↓
 10pt      Weak    OK      OK      Weak
 15pt      OK      GOOD    ★BEST   GOOD
 20pt      OK      GOOD    GOOD    GOOD
 25pt      Weak    GOOD    GOOD    OK
 30pt      Weak    OK      GOOD    OK
```

**The sweet spot:** moderate distance (not too close, not too far) with a moderate stop. Too tight a stop killed win rate. Too loose a stop let losers run. Too close a distance = noise trades. Too far = too few trades.

### Target offset experiment:

| Offset | Win Rate | Profit Factor | Sharpe | Max Drawdown | Verdict |
|--------|----------|---------------|--------|-------------|---------|
| 0 (exact) | 73.8% | 2.35 | 4.13 | $2,483 | **Best overall** |
| 2 pts | 73.8% | 2.29 | 3.95 | $2,493 | Similar |
| 3 pts | 74.6% | 2.32 | 3.92 | **$1,969** | **Lowest drawdown** |
| 5 pts | 73.8% | 2.24 | 3.53 | $1,961 | Gives up too much profit |

**The AI's recommendation:** *"Offset 0 and 3 are both defensible. Zero maximizes expected value. Three minimizes worst-case drawdown. This is a risk preference question, not a data question."* The human chose 0.

---

## Phase 4: Exit Strategy Refinement

**Experiments: 9 | Goal: can we improve the exit?**

With entries optimized, we stress-tested the exit. The trader's instinct was to add trailing stops or complex exit conditions. The AI tested them all:

| Exit Method | Win Rate | Profit Factor | Max Drawdown | Verdict |
|-------------|----------|---------------|-------------|---------|
| **Simple: stop + target** | **73.8%** | **2.35** | **$2,483** | **Baseline** |
| Trailing stop (wide) | 65.9% | 2.06 | $2,971 | **Worse on every metric** |
| Trailing stop (tight) | 60.5% | 2.11 | $2,893 | Even worse |
| Momentum-based exit | 45.1% | 1.85 | $1,502 | Lowest drawdown, but halved win rate |
| Structure break exit | 52.0% | 2.10 | $1,397 | Same problem |
| Trailing + momentum | 43.1% | 1.69 | $1,420 | Over-complex, worst PF |

**The counterintuitive finding:** Every "sophisticated" exit was worse than the simple one. The AI's explanation: *"This is a mean-reversion strategy. The target IS the mean. Trailing stops cut the move short — they're designed for trend-following, not reversion. The simple exit is correct because it matches the strategy's thesis."*

The trader initially resisted this. Adding a trailing stop *felt* safer. But the data was unambiguous. **Sometimes the best optimization is deciding not to optimize.**

---

## Phase 5: Entry Refinement — "Can we make it even better?"

**Experiments: 16 | Goal: fine-tune entry conditions**

### Signal method deep dive

Remember Phase 1 tested five signal methods? With filters now in place, we retested:

| Signal | Trades/Day | Win Rate | Profit Factor | $/Trade | Verdict |
|--------|-----------|----------|---------------|---------|---------|
| Method B | 2.8 | 69.7% | 1.84 | $121 | Good |
| **Method D** | **2.5** | **75.0%** | **3.03** | **$256** | **Best per-trade** |
| Method A | 1.1 | 66.7% | 1.09 | $17 | **No edge — DROP** |
| B + D combined | 4.5 | 73.8% | 2.35 | $175 | Best balance |

**Discovery:** Method A, which looked reasonable in Phase 1, had *zero edge* once quality filters were applied. It was just adding noise. We dropped it entirely — reducing the signal set from "any of five" to "two specific patterns."

### Overextension threshold sensitivity

| Threshold | Trades/Day | Win Rate | Profit Factor | Sharpe | Character |
|-----------|-----------|----------|---------------|--------|-----------|
| Low (loose) | 6.2 | 71.9% | 2.05 | 3.66 | More trades, slightly weaker |
| **Medium** | **4.5** | **73.8%** | **2.35** | **4.13** | **Sweet spot** |
| Medium-high | 3.0 | 71.6% | 2.53 | 4.39 | Higher quality, fewer trades |
| High (strict) | 2.5 | 73.1% | 3.08 | 5.15 | **Best quality, fewest trades** |

This is a classic quality vs. quantity tradeoff. The AI presented it as a dial, not a single answer.

### Direction split

| Direction | Win Rate | Profit Factor | Sharpe | $/Trade | Max Drawdown |
|-----------|----------|---------------|--------|---------|-------------|
| **Short** | **77.6%** | **3.01** | **4.95** | **$223** | **$1,300** |
| Long | 70.3% | 1.90 | 3.33 | $131 | $2,432 |
| Both | 73.8% | 2.35 | 4.13 | $175 | $2,483 |

Shorts dominated — nearly 78% win rate, 3x profit factor, half the drawdown of longs. But we didn't drop longs (yet). This asymmetry informed the risk management phase.

---

## Phase 6: Two-Year Validation — "Is the edge real?"

**Goal: test on 2.5 years of unseen data (430 trading days, 1.34M bars)**

Everything up to this point was optimized on ~150 days of data. The real test: does it hold on 2+ years?

| Metric | Optimization Period | 2-Year Full Period |
|--------|-------------------|--------------------|
| Trades/day | 4.5 | 2.3 |
| Win Rate | 73.8% | 69.1% |
| Profit Factor | 2.35 | 1.68 |
| Sharpe | 4.13 | 2.68 |
| Max Drawdown | $2,483 | $6,748 |

**Metrics degraded but the edge held.** This is *expected* — in-sample always looks better than out-of-sample. The important thing: still profitable, still above 2.5 Sharpe, still 69% win rate over 1,000+ trades across 2.5 years.

### Monthly consistency

Over 21 months of trading:
- **18 profitable months** (86%)
- **3 losing months** — all with small losses
- Best month: +$38,854
- Worst month: -$912
- Both long and short sides contributed roughly equally over the full period

The short-side dominance from the optimization period **did not hold** over 2 years. Both directions were profitable. The AI flagged this: *"The short dominance in optimization was likely a regime effect, not a structural edge. Over 2 years, both sides contribute. Trade both."*

---

## Phase 7: Drawdown Control — "How do we manage risk?"

**Experiments: 36 | Goal: cut max drawdown by 50%**

The 2-year validation showed a $6,748 max drawdown. The trader wanted it under $3,500. The AI tested six approaches:

| Approach | MaxDD Result | P&L Impact | Verdict |
|----------|-------------|------------|---------|
| Tighter stops | Still >$5,000 | Moderate | **FAILED** — drawdowns come from loss clusters, not single big losses |
| Cooldown after loss | **Increased** MaxDD | Negative | **FAILED** — skips recovery trades |
| Daily loss limit | ~$4,600 | -28% P&L | Partial |
| Max consecutive losses | Barely changed | None | **FAILED** |
| Asymmetric stops | Marginal | Marginal | **FAILED** |
| Stricter entry threshold | ~$6,200 | -10% P&L | Partial |

**None of these worked alone.** The AI's analysis: *"Your drawdowns aren't from single big losses — they're from clusters of small losses on consecutive days. No single lever fixes that. You need to combine selectivity (fewer, better trades) with loss mitigation (stop trading when the day goes bad)."*

The winning combination: stricter entry threshold + cooldown after stops + daily loss cap.

| Config | Trades/Day | P&L | Win Rate | PF | Sharpe | Max Drawdown |
|--------|-----------|-----|----------|-----|--------|-------------|
| Maximum P&L | 2.3 | $113,505 | 69.1% | 1.68 | 2.68 | $6,748 |
| Higher Quality | 1.7 | $102,365 | 70.4% | 1.84 | 3.02 | $6,260 |
| **Drawdown Controlled** | **1.0** | **$68,221** | **70.7%** | **2.00** | **3.72** | **$3,503** |

Three configurations, three risk profiles. The trader now has a dial: more P&L with more risk, or less P&L with a smoother ride. **That's not a parameter optimization — that's a business decision.**

---

## The Numbers: What AutoForge Made Possible

| Metric | Before AutoForge | After AutoForge |
|--------|-----------------|-----------------|
| Concept | Vague intuition | Precise, coded rules |
| Signal methods tested | 0 | 5 |
| Filters evaluated | 0 | 8 individual, 15+ combinations |
| Parameter combinations swept | 0 | 1,400+ |
| Exit strategies tested | 0 | 9 |
| Total experiments | 0 | **200+** |
| Validation period | None | 2.5 years (430 trading days) |
| Time to complete | Would take months manually | Days |

### Key decisions the AI surfaced that the human didn't anticipate:

1. **One signal method had zero edge** — looked fine in isolation, dead weight with filters
2. **Trailing stops hurt** — counterintuitive for a trader who always uses them
3. **A "sophisticated" filter produced zero trades** — wrong calibration for this bar type
4. **Short-side dominance was temporary** — a regime effect, not structural
5. **Drawdowns come from clusters, not single losses** — no single fix works
6. **Adding a third filter was redundant** — diminishing returns caught early

---

## The Methodology

This case study demonstrates AutoForge's core loop:

```
 ┌─────────────────────────────────────────────────┐
 │  1. DESCRIBE — Human shares intuition            │
 │  2. INTERVIEW — AI asks clarifying questions      │
 │  3. BASELINE — Test the raw concept               │
 │  4. DISCOVER — AI suggests filters & conditions   │
 │  5. SWEEP — Systematically explore parameter space │
 │  6. REFINE — Test entries, exits, edge cases       │
 │  7. VALIDATE — Out-of-sample on unseen data        │
 │  8. HARDEN — Risk management & drawdown control    │
 │  9. DECIDE — Human picks the risk profile          │
 └─────────────────────────────────────────────────┘
```

The AI doesn't replace the trader's judgment. It amplifies it. The trader brought the core idea and made the final decisions. The AI brought breadth — testing 200+ variations that would take months by hand, catching dead ends early, and surfacing patterns the human might miss.

**AutoForge doesn't give you an edge. You bring the edge. AutoForge tells you if it's real.**
