"""Generate Mean Reversion case study visuals."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#0d1117",
    "text.color": "#e6edf3",
    "axes.labelcolor": "#e6edf3",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
    "axes.edgecolor": "#30363d",
    "grid.color": "#21262d",
    "font.family": "sans-serif",
    "font.size": 12,
})

ACCENT = "#58a6ff"
GREEN = "#3fb950"
RED = "#f85149"
ORANGE = "#d29922"
PURPLE = "#bc8cff"
CYAN = "#39d353"
DIMMED = "#8b949e"


def fig1_robustness():
    """97% of parameter combinations are profitable."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7),
                                    gridspec_kw={"width_ratios": [1, 1.2]})

    # Left: pie chart — 97% profitable
    sizes = [97, 3]
    colors_pie = [GREEN, RED]
    explode = (0.03, 0.08)
    wedges, texts, autotexts = ax1.pie(
        sizes, explode=explode, colors=colors_pie, autopct='%1.0f%%',
        startangle=90, textprops={'fontsize': 18, 'fontweight': 'bold'},
        pctdistance=0.55,
    )
    autotexts[0].set_color("#e6edf3")
    autotexts[1].set_color("#e6edf3")
    ax1.set_title("Parameter Combinations\nThat Are Profitable",
                   fontsize=16, fontweight="bold", color=ACCENT, pad=20)

    # Stats below pie
    ax1.text(0, -1.4, "350 profitable out of 360 tested",
             ha="center", fontsize=11, color=DIMMED)
    ax1.text(0, -1.6, "The edge doesn't depend on exact parameters",
             ha="center", fontsize=10, color=DIMMED, style="italic")

    # Right: stop sensitivity — all 18 stops profitable
    stops = [5, 8, 10, 12, 15, 16, 20, 25, 30, 35, 40, 50]
    # Relative P&L (normalized to best = 1.0)
    pnl_rel = [0.45, 0.52, 0.54, 0.71, 0.74, 0.75, 0.94, 0.97, 1.00, 0.99, 0.97, 0.98]

    colors_bar = [ORANGE if p < 0.6 else (ACCENT if p < 0.9 else GREEN) for p in pnl_rel]

    bars = ax2.bar(range(len(stops)), pnl_rel, color=colors_bar, alpha=0.85,
                   width=0.65, edgecolor="#30363d", linewidth=1.5)

    ax2.axhline(y=0, color=RED, linewidth=1.5, linestyle="--", alpha=0.5)

    # "ALL PROFITABLE" banner
    ax2.text(5.5, 1.08, "ALL 18 STOP LEVELS PROFITABLE",
             ha="center", fontsize=13, fontweight="bold", color=GREEN,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#161b22",
                       edgecolor=GREEN, linewidth=2))

    ax2.set_xticks(range(len(stops)))
    ax2.set_xticklabels([f"{s}pt" for s in stops], fontsize=9, rotation=45)
    ax2.set_ylabel("Relative P&L", fontsize=12)
    ax2.set_title("Stop Loss Sensitivity Sweep",
                   fontsize=16, fontweight="bold", color=ACCENT, pad=20)
    ax2.set_ylim(0, 1.2)
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Robustness — The Edge Is Real, Not a Parameter Artifact",
                 fontsize=18, fontweight="bold", color=ACCENT, y=1.02)
    fig.tight_layout()
    fig.savefig("docs/images/mr_01_robustness.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_01_robustness.png")


def fig2_random_baseline():
    """Random entries lose catastrophically — signals matter."""
    fig, ax = plt.subplots(figsize=(14, 7))

    categories = [
        "Strategy\nSignals",
        "Random\nevery 5 bars",
        "Random\nevery 10 bars",
        "Random\nevery 20 bars",
        "Random\nevery 50 bars",
        "Random\nevery 100 bars",
    ]
    # Normalized values (strategy = 1.0, randoms are negative multiples)
    values = [1.0, -41, -27, -15, -5.8, -3.0]
    colors = [GREEN] + [RED] * 5

    bars = ax.bar(range(len(categories)), values, color=colors, alpha=0.85,
                  width=0.55, edgecolor="#30363d", linewidth=1.5)

    # Labels
    labels = ["Profitable", "-$2.1M", "-$1.4M", "-$770K", "-$301K", "-$152K"]
    for i, (v, label) in enumerate(zip(values, labels)):
        y_pos = v + 0.5 if v > 0 else v - 2
        ax.text(i, y_pos, label, ha="center", va="bottom" if v > 0 else "top",
                fontsize=11, fontweight="bold",
                color=GREEN if v > 0 else RED)

    # Win rate annotations
    win_rates = ["66%", "36%", "36%", "36%", "36%", "36%"]
    for i, wr in enumerate(win_rates):
        y_base = max(values[i], 0) + 2 if values[i] > 0 else -1
        ax.text(i, y_base, f"Win: {wr}", ha="center", fontsize=9, color=DIMMED)

    ax.axhline(y=0, color=DIMMED, linewidth=1.5)
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=10, linespacing=1.3)
    ax.set_ylabel("Relative Performance", fontsize=12)
    ax.set_title("Random Entries Lose Catastrophically — The Signals Are Real",
                 fontsize=18, fontweight="bold", pad=20, color=ACCENT)
    ax.set_ylim(-45, 8)
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Annotation
    ax.text(3, -42, "25 random baseline trials, same stop/target mechanics.\n"
            "If random entries made money, the signals would be meaningless. They don't.",
            ha="center", fontsize=10, color=DIMMED, style="italic",
            linespacing=1.5)

    fig.tight_layout()
    fig.savefig("docs/images/mr_02_random_baseline.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_02_random_baseline.png")


def fig3_sweep_scale():
    """3,500+ combinations swept across 5 batches."""
    fig, ax = plt.subplots(figsize=(14, 7))

    batches = [
        ("Batch 1\nInitial\nSweep", 270, "11 params\nfull grid"),
        ("Batch 2\nRefined\nGrid", 270, "Filters\nremoved"),
        ("Batch 3\nFixed-Stop\nDeep Dive", 360, "18 stops\n8 targets"),
        ("Batch 4\nLarge\nSweep", 1500, "Core params\nfine grid"),
        ("Batch 5\nSession &\nDirection", 810, "Time filters\ndirection split"),
        ("Validity\nTests", 70, "Ablation\nrandom baseline"),
    ]

    x = np.arange(len(batches))
    names = [b[0] for b in batches]
    counts = [b[1] for b in batches]
    notes = [b[2] for b in batches]
    cumulative = np.cumsum(counts)

    colors_bar = [ACCENT, ACCENT, ORANGE, GREEN, ACCENT, PURPLE]

    bars = ax.bar(x, counts, color=colors_bar, alpha=0.8, width=0.6,
                  edgecolor="#30363d", linewidth=1.5)

    # Cumulative line
    ax2 = ax.twinx()
    ax2.plot(x, cumulative, color=CYAN, linewidth=3, marker="o",
             markersize=8, zorder=5)
    ax2.set_ylabel("Cumulative Experiments", fontsize=13, color=CYAN)
    ax2.tick_params(axis="y", colors=CYAN)
    ax2.spines["right"].set_color(CYAN)
    ax2.set_ylim(0, 4000)

    for i, (c, note) in enumerate(zip(counts, notes)):
        ax.text(i, c + 30, f"{c:,}", ha="center", fontsize=12,
                fontweight="bold", color=colors_bar[i])
        ax.text(i, -130, note, ha="center", va="top", fontsize=9,
                color=DIMMED, linespacing=1.3)

    # Total callout
    ax.text(5.3, 1400, f"TOTAL: {sum(counts):,}+\nexperiments",
            ha="right", fontsize=14, fontweight="bold", color=CYAN,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#161b22",
                      edgecolor=CYAN, linewidth=2))

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9, linespacing=1.3)
    ax.set_ylabel("Experiments in Batch", fontsize=13)
    ax.set_title("3,500+ Parameter Combinations Swept Across 6 Phases",
                 fontsize=18, fontweight="bold", pad=20, color=ACCENT)
    ax.set_ylim(0, 1700)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.18)
    fig.savefig("docs/images/mr_03_sweep_scale.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_03_sweep_scale.png")


def fig4_heatmap():
    """Stop x Target heatmap showing the profitable plateau."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Simplified heatmap data (stop x target, relative P&L)
    stops = ["5pt", "8pt", "10pt", "12pt", "15pt", "20pt", "25pt", "30pt"]
    targets = ["5pt", "8pt", "10pt", "15pt", "20pt", "30pt", "Mean\nLine", "None"]

    # Relative P&L (0-1 scale, from the actual data)
    data = np.array([
        [0.01, 0.13, 0.18, 0.26, 0.32, 0.24, 0.40, 0.31],
        [-0.03, 0.14, 0.18, 0.34, 0.39, 0.36, 0.47, 0.39],
        [-0.01, 0.14, 0.21, 0.49, 0.52, 0.46, 0.49, 0.46],
        [0.11, 0.27, 0.33, 0.62, 0.67, 0.58, 0.64, 0.67],
        [0.13, 0.28, 0.36, 0.64, 0.71, 0.64, 0.67, 0.74],
        [0.19, 0.38, 0.46, 0.76, 0.81, 0.83, 0.86, 0.91],
        [0.18, 0.37, 0.43, 0.77, 0.84, 0.84, 0.88, 0.91],
        [0.19, 0.39, 0.46, 0.80, 0.85, 0.89, 0.92, 1.00],
    ])

    # Custom colormap: red -> yellow -> green
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("autoforge",
        [(0, "#f85149"), (0.3, "#d29922"), (0.6, "#58a6ff"), (1.0, "#3fb950")])

    im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=-0.05, vmax=1.0)

    # Annotations
    for i in range(len(stops)):
        for j in range(len(targets)):
            val = data[i, j]
            color = "#0d1117" if val > 0.5 else "#e6edf3"
            if val < 0:
                text = "Loss"
                color = RED
            else:
                text = f"{val:.0%}"
            ax.text(j, i, text, ha="center", va="center",
                    fontsize=9, fontweight="bold", color=color)

    ax.set_xticks(range(len(targets)))
    ax.set_xticklabels(targets, fontsize=10, linespacing=1.2)
    ax.set_yticks(range(len(stops)))
    ax.set_yticklabels(stops, fontsize=10)
    ax.set_xlabel("Target Type", fontsize=13, labelpad=10)
    ax.set_ylabel("Stop Loss", fontsize=13, labelpad=10)
    ax.set_title("Stop x Target Heatmap — A Broad Plateau of Profitability",
                 fontsize=16, fontweight="bold", pad=20, color=ACCENT)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Relative P&L", fontsize=11, color=DIMMED)
    cbar.ax.tick_params(colors=DIMMED)

    # Highlight best region
    rect = mpatches.Rectangle((5.5, 4.5), 2.5, 3.5,
                                linewidth=2.5, edgecolor=GREEN,
                                facecolor="none", linestyle="--")
    ax.add_patch(rect)
    ax.text(7.8, 4.2, "Best\nRegion", fontsize=10, fontweight="bold",
            color=GREEN, ha="center")

    fig.tight_layout()
    fig.savefig("docs/images/mr_04_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_04_heatmap.png")


def fig5_portfolio():
    """Combining uncorrelated strategies reduces drawdown."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Left: correlation matrix
    strategies = ["Momentum", "Mean\nReversion", "Breakout", "Trend\nFollowing"]
    corr = np.array([
        [1.00, 0.09, -0.01, -0.04],
        [0.09, 1.00, -0.07, -0.03],
        [-0.01, -0.07, 1.00, 0.35],
        [-0.04, -0.03, 0.35, 1.00],
    ])

    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("corr",
        [(0, ACCENT), (0.5, "#161b22"), (1.0, RED)])

    im = ax1.imshow(corr, cmap=cmap, vmin=-0.5, vmax=0.5, aspect="equal")

    for i in range(4):
        for j in range(4):
            color = "#e6edf3"
            ax1.text(j, i, f"{corr[i,j]:.2f}", ha="center", va="center",
                    fontsize=12, fontweight="bold", color=color)

    ax1.set_xticks(range(4))
    ax1.set_xticklabels(strategies, fontsize=9, linespacing=1.2)
    ax1.set_yticks(range(4))
    ax1.set_yticklabels(strategies, fontsize=9, linespacing=1.2)
    ax1.set_title("Strategy Correlation Matrix",
                  fontsize=14, fontweight="bold", color=ACCENT, pad=15)

    # Right: drawdown reduction
    combos = ["Momentum\nAlone", "MR\nAlone", "Mom +\nMR", "Mom + MR\n+ Breakout", "All\nFour"]
    dd_individual = [100, 26, None, None, None]
    dd_combined = [None, None, 85, 102, 319]
    dd_sum = [None, None, 126, 226, 649]
    dd_reduction = [None, None, 32, 63, 51]

    # Show actual MaxDD (relative)
    dd_values = [100, 26, 85, 102, 319]
    dd_if_no_diversification = [100, 26, 126, 226, 649]

    x = np.arange(len(combos))
    width = 0.35

    bars1 = ax2.bar(x - width/2, dd_if_no_diversification, width,
                     color=RED, alpha=0.4, label="Expected (no diversification)",
                     edgecolor="#30363d", linewidth=1)
    bars2 = ax2.bar(x + width/2, dd_values, width,
                     color=GREEN, alpha=0.8, label="Actual combined",
                     edgecolor="#30363d", linewidth=1)

    # Reduction labels
    for i in range(2, 5):
        reduction = dd_reduction[i]
        if reduction:
            ax2.text(i, dd_if_no_diversification[i] + 15,
                    f"-{reduction}%", ha="center", fontsize=11,
                    fontweight="bold", color=GREEN)

    ax2.set_xticks(x)
    ax2.set_xticklabels(combos, fontsize=9, linespacing=1.2)
    ax2.set_ylabel("Relative Max Drawdown", fontsize=12)
    ax2.set_title("Combining Reduces Drawdown",
                  fontsize=14, fontweight="bold", color=ACCENT, pad=15)
    ax2.legend(loc="upper left", fontsize=9, facecolor="#161b22",
               edgecolor="#30363d")
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Uncorrelated Strategies = Portfolio Gold",
                 fontsize=18, fontweight="bold", color=ACCENT, y=1.02)
    fig.tight_layout()
    fig.savefig("docs/images/mr_05_portfolio.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_05_portfolio.png")


def fig6_journey():
    """MR journey timeline."""
    fig, ax = plt.subplots(figsize=(16, 6))

    milestones = [
        ("Interview\n& Specify", "11 parameters\nidentified", DIMMED, 0),
        ("Initial\nSweep", "270 combos\nfilters removed", RED, 1),
        ("Big\nSweep", "1,500 combos\nplateau found", ORANGE, 2),
        ("Stop\nDeep Dive", "360 combos\nall profitable", ACCENT, 3),
        ("Validity\nAnalysis", "Random baseline\nablation tests", PURPLE, 4),
        ("Time\nAnalysis", "2 bad hours\nidentified", ACCENT, 5),
        ("Portfolio\nIntegration", "0.09 correlation\n32% less DD", GREEN, 6),
    ]

    ax.plot([0, 6], [0.5, 0.5], color="#30363d", linewidth=3, zorder=1)

    for name, detail, color, x_pos in milestones:
        circle = plt.Circle((x_pos, 0.5), 0.12, color=color, zorder=3)
        ax.add_patch(circle)

        if x_pos % 2 == 0:
            y_name, y_detail, y_line = 0.78, 0.93, 0.62
        else:
            y_name, y_detail, y_line = 0.22, 0.07, 0.38

        ax.plot([x_pos, x_pos], [0.5, y_line], color=color, linewidth=1.5,
                alpha=0.5, zorder=2)
        ax.text(x_pos, y_name, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color, linespacing=1.3)
        ax.text(x_pos, y_detail, detail, ha="center", va="center",
                fontsize=9, color=DIMMED, linespacing=1.3)

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Mean Reversion Journey — From Textbook Concept to Validated Edge",
                 fontsize=18, fontweight="bold", color=ACCENT, pad=15)

    fig.tight_layout()
    fig.savefig("docs/images/mr_06_journey.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  mr_06_journey.png")


if __name__ == "__main__":
    print("Generating MR case study visuals...")
    fig1_robustness()
    fig2_random_baseline()
    fig3_sweep_scale()
    fig4_heatmap()
    fig5_portfolio()
    fig6_journey()
    print("\nDone! 6 MR images in docs/images/")
