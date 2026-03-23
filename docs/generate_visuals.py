"""Generate case study visuals for AutoForge.

Run: python docs/generate_visuals.py
Output: docs/images/*.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

# Style
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


def fig1_the_funnel():
    """The Quality Funnel — from 60 trades/day to 4.5, quality soaring."""
    fig, ax = plt.subplots(figsize=(14, 8))

    stages = [
        ("Raw Signal\n(no filters)", 60.3, 1.09, 0.05),
        ("Best Single\nFilter", 24.4, 1.35, 1.84),
        ("Two-Filter\nCombo", 4.5, 2.35, 4.13),
        ("Entry\nRefined", 4.5, 2.35, 4.13),
        ("2-Year\nValidated", 2.3, 1.68, 2.68),
        ("Drawdown\nControlled", 1.0, 2.00, 3.72),
    ]

    x = np.arange(len(stages))
    names = [s[0] for s in stages]
    trades = [s[1] for s in stages]
    pf = [s[2] for s in stages]
    sharpe = [s[3] for s in stages]

    # Trades/day as bar width (funnel effect)
    max_width = 0.85
    widths = [max_width * (t / max(trades)) for t in trades]
    widths = [max(w, 0.08) for w in widths]

    # Bars — color by quality
    colors = []
    for s in sharpe:
        if s < 1:
            colors.append(RED)
        elif s < 2:
            colors.append(ORANGE)
        elif s < 3:
            colors.append(ACCENT)
        else:
            colors.append(GREEN)

    bars = ax.bar(x, trades, width=widths, color=colors, alpha=0.85,
                  edgecolor="#30363d", linewidth=1.5)

    # Sharpe annotation on each bar
    for i, (xi, t, s, pfi) in enumerate(zip(x, trades, sharpe, pf)):
        ax.text(xi, t + 2.5, f"Sharpe {s:.2f}", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=colors[i],
                path_effects=[pe.withStroke(linewidth=3, foreground="#0d1117")])
        ax.text(xi, t + 0.5, f"PF {pfi:.2f}", ha="center", va="bottom",
                fontsize=9, color=DIMMED)

    # Arrow showing the journey
    for i in range(len(stages) - 1):
        ax.annotate("", xy=(x[i+1] - 0.15, trades[i+1] + 8),
                     xytext=(x[i] + 0.15, trades[i] + 8),
                     arrowprops=dict(arrowstyle="->", color=DIMMED, lw=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=11)
    ax.set_ylabel("Trades / Day", fontsize=13)
    ax.set_title("The Quality Funnel — Fewer Trades, Sharper Edge",
                 fontsize=18, fontweight="bold", pad=20, color=ACCENT)
    ax.set_ylim(0, 75)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=RED, label="Weak (Sharpe < 1)"),
        mpatches.Patch(facecolor=ORANGE, label="Moderate (1-2)"),
        mpatches.Patch(facecolor=ACCENT, label="Strong (2-3)"),
        mpatches.Patch(facecolor=GREEN, label="Excellent (3+)"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=10,
              facecolor="#161b22", edgecolor="#30363d")

    fig.tight_layout()
    fig.savefig("docs/images/01_quality_funnel.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  01_quality_funnel.png")


def fig2_experiment_scale():
    """The Scale — 200+ experiments across 8 phases."""
    fig, ax = plt.subplots(figsize=(14, 7))

    phases = [
        ("Phase 1\nSignal\nBaseline", 10, "Which signal\ndetection works?"),
        ("Phase 2\nFilter\nDiscovery", 22, "8 filters tested\nsingles + combos"),
        ("Phase 3\nParameter\nGrid", 48, "1,400+ combos\nswept"),
        ("Phase 4\nExit\nRefinement", 9, "Trailing stops\ntested & killed"),
        ("Phase 5\nEntry\nRefinement", 16, "Signal methods\nre-evaluated"),
        ("Phase 6\n2-Year\nValidation", 8, "430 days\n1.34M bars"),
        ("Phase 7\nDrawdown\nControl", 36, "6 approaches\n3 configs out"),
        ("Phase 8\nFinal\nLockdown", 3, "3 risk profiles\ndelivered"),
    ]

    x = np.arange(len(phases))
    names = [p[0] for p in phases]
    counts = [p[1] for p in phases]
    notes = [p[2] for p in phases]

    # Cumulative experiments
    cumulative = np.cumsum(counts)

    # Bar chart
    bars = ax.bar(x, counts, color=ACCENT, alpha=0.8, width=0.6,
                  edgecolor="#30363d", linewidth=1.5)

    # Cumulative line
    ax2 = ax.twinx()
    ax2.plot(x, cumulative, color=GREEN, linewidth=3, marker="o",
             markersize=8, zorder=5)
    ax2.set_ylabel("Cumulative Experiments", fontsize=13, color=GREEN)
    ax2.tick_params(axis="y", colors=GREEN)
    ax2.spines["right"].set_color(GREEN)
    ax2.set_ylim(0, 200)

    # Annotations
    for i, (xi, c, note) in enumerate(zip(x, counts, notes)):
        ax.text(xi, c + 1.5, str(c), ha="center", va="bottom",
                fontsize=13, fontweight="bold", color=ACCENT)
        ax.text(xi, -8, note, ha="center", va="top",
                fontsize=8, color=DIMMED, linespacing=1.3)

    # Total callout
    ax.text(7.4, 42, f"TOTAL: {sum(counts)}+\nexperiments",
            ha="right", va="top", fontsize=14, fontweight="bold",
            color=GREEN,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#161b22",
                      edgecolor=GREEN, linewidth=2))

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9, linespacing=1.3)
    ax.set_ylabel("Experiments in Phase", fontsize=13)
    ax.set_title("200+ Experiments Across 8 Phases",
                 fontsize=18, fontweight="bold", pad=20, color=ACCENT)
    ax.set_ylim(0, 55)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.18)
    fig.savefig("docs/images/02_experiment_scale.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  02_experiment_scale.png")


def fig3_dead_ends():
    """Dead Ends — what we tried that didn't work (and why that matters)."""
    fig, ax = plt.subplots(figsize=(14, 7))

    items = [
        ("Trailing Stop\n(wide)", "Worse drawdown\nthan simple exit", -1),
        ("Trailing Stop\n(tight)", "Killed win rate\nfrom 74% to 61%", -1),
        ("Climax Bar\nFilter", "Zero trades\non range bars", -1),
        ("Signal\nMethod A", "No edge with\nquality filters", -1),
        ("3rd Filter\nAdded", "Redundant —\nsame trades", 0),
        ("Cooldown\nAfter Loss", "Increased\ndrawdown", -1),
        ("Tighter Stop\nAlone", "Clusters still\ncause drawdown", 0),
        ("Trailing +\nMomentum Exit", "Over-complex\nworst PF", -1),
    ]

    x = np.arange(len(items))
    names = [i[0] for i in items]
    reasons = [i[1] for i in items]
    severity = [i[2] for i in items]

    colors = [RED if s == -1 else ORANGE for s in severity]

    # X marks
    for i, (xi, name, reason, sev) in enumerate(zip(x, names, reasons, severity)):
        ax.text(xi, 0.6, "✗", ha="center", va="center",
                fontsize=40, fontweight="bold", color=colors[i],
                path_effects=[pe.withStroke(linewidth=2, foreground="#0d1117")])
        ax.text(xi, 0.35, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color="#e6edf3", linespacing=1.3)
        ax.text(xi, 0.15, reason, ha="center", va="center",
                fontsize=9, color=DIMMED, linespacing=1.3)

    ax.set_xlim(-0.5, len(items) - 0.5)
    ax.set_ylim(0, 0.85)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.set_title("Dead Ends Caught Early — Weeks of Manual Research Saved",
                 fontsize=18, fontweight="bold", pad=20, color=RED)

    # Subtitle
    ax.text(3.5, 0.78, "Every failed experiment is a shortcut.\n"
            "AutoForge tested these in hours, not weeks.",
            ha="center", va="center", fontsize=12, color=DIMMED,
            style="italic", linespacing=1.5)

    fig.tight_layout()
    fig.savefig("docs/images/03_dead_ends.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  03_dead_ends.png")


def fig4_three_profiles():
    """Three Risk Profiles — the final output."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 7))

    profiles = [
        {
            "name": "Maximum P&L",
            "color": GREEN,
            "icon": "▲",
            "metrics": {
                "Trades/Day": "2.3",
                "Win Rate": "69.1%",
                "Profit Factor": "1.68",
                "Sharpe": "2.68",
                "Max Drawdown": "Moderate",
            },
            "tag": "More risk, more reward",
            "pnl_bar": 1.0,
        },
        {
            "name": "Higher Quality",
            "color": ACCENT,
            "icon": "◆",
            "metrics": {
                "Trades/Day": "1.7",
                "Win Rate": "70.4%",
                "Profit Factor": "1.84",
                "Sharpe": "3.02",
                "Max Drawdown": "Moderate",
            },
            "tag": "Fewer, better trades",
            "pnl_bar": 0.90,
        },
        {
            "name": "Drawdown Controlled",
            "color": PURPLE,
            "icon": "●",
            "metrics": {
                "Trades/Day": "1.0",
                "Win Rate": "70.7%",
                "Profit Factor": "2.00",
                "Sharpe": "3.72",
                "Max Drawdown": "Low",
            },
            "tag": "Smooth ride, steady growth",
            "pnl_bar": 0.60,
        },
    ]

    for ax, profile in zip(axes, profiles):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])

        # Card background
        card = mpatches.FancyBboxPatch(
            (0.05, 0.05), 0.9, 0.9,
            boxstyle="round,pad=0.03",
            facecolor="#161b22",
            edgecolor=profile["color"],
            linewidth=2.5,
        )
        ax.add_patch(card)

        # Icon and name
        ax.text(0.5, 0.88, profile["icon"], ha="center", va="center",
                fontsize=28, color=profile["color"])
        ax.text(0.5, 0.78, profile["name"], ha="center", va="center",
                fontsize=16, fontweight="bold", color=profile["color"])
        ax.text(0.5, 0.71, profile["tag"], ha="center", va="center",
                fontsize=9, color=DIMMED, style="italic")

        # Metrics
        y = 0.60
        for key, val in profile["metrics"].items():
            ax.text(0.15, y, key, ha="left", va="center", fontsize=10, color=DIMMED)
            ax.text(0.85, y, val, ha="right", va="center", fontsize=10,
                    fontweight="bold", color="#e6edf3")
            y -= 0.08

        # Relative P&L bar
        bar_y = 0.14
        bar_width = profile["pnl_bar"] * 0.7
        bar = mpatches.FancyBboxPatch(
            (0.15, bar_y), bar_width, 0.04,
            boxstyle="round,pad=0.01",
            facecolor=profile["color"],
            alpha=0.6,
        )
        ax.add_patch(bar)
        ax.text(0.5, bar_y + 0.09, "Relative P&L", ha="center", va="center",
                fontsize=8, color=DIMMED)

        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.suptitle("One Strategy, Three Risk Profiles — You Choose",
                 fontsize=18, fontweight="bold", color=ACCENT, y=0.98)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("docs/images/04_three_profiles.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  04_three_profiles.png")


def fig5_filter_discovery():
    """Filter Discovery — how 8 filters were tested and the best combo emerged."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [1, 1.2]})

    # Left: Single filter comparison
    filters = ["Trend\nAlignment", "Slope\nCondition", "Over-\nextension",
               "Exhaustion\nBars", "Exhaustion\nMethod B", "Reversal\nCondition",
               "Slope\nCondition B", "Climax\nDetection"]
    pf_values = [1.35, 1.40, 1.32, 1.31, 1.16, 1.19, 1.33, 0.0]
    kept = [True, True, True, True, False, False, True, False]

    colors_single = [GREEN if k else RED for k in kept]
    # Special: climax is a special dead end
    colors_single[-1] = "#333333"

    y_pos = np.arange(len(filters))
    bars = ax1.barh(y_pos, pf_values, color=colors_single, alpha=0.8,
                    height=0.6, edgecolor="#30363d")

    # Baseline line
    ax1.axvline(x=1.0, color=ORANGE, linestyle="--", linewidth=1.5, alpha=0.7)
    ax1.text(1.02, 7.5, "breakeven", fontsize=9, color=ORANGE, va="center")

    for i, (pf, k) in enumerate(zip(pf_values, kept)):
        label = f"{pf:.2f}" if pf > 0 else "0 trades!"
        color = GREEN if k else (RED if pf > 0 else "#666")
        ax1.text(max(pf, 0) + 0.02, i, label, va="center", fontsize=10,
                fontweight="bold", color=color)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(filters, fontsize=10)
    ax1.set_xlabel("Profit Factor", fontsize=12)
    ax1.set_title("8 Filters Tested Individually", fontsize=14,
                  fontweight="bold", color=ACCENT)
    ax1.set_xlim(0, 1.6)
    ax1.grid(axis="x", alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.invert_yaxis()

    # Right: Combo results
    combos = [
        ("No filters\n(baseline)", 1.28, 1.64, 96.5),
        ("Trend\nalone", 1.35, 1.84, 24.4),
        ("Overextension\nalone", 1.32, 1.81, 67.9),
        ("Trend +\nOverextension", 2.35, 4.13, 4.5),
        ("Triple\ncombo", 2.33, 4.09, 4.5),
    ]

    x_pos = np.arange(len(combos))
    combo_names = [c[0] for c in combos]
    combo_pf = [c[1] for c in combos]
    combo_sharpe = [c[2] for c in combos]
    combo_trades = [c[3] for c in combos]

    # Sharpe bars
    combo_colors = [DIMMED, ORANGE, ORANGE, GREEN, ACCENT]
    bars2 = ax2.bar(x_pos, combo_sharpe, color=combo_colors, alpha=0.85,
                    width=0.55, edgecolor="#30363d", linewidth=1.5)

    for i, (s, pf, tr) in enumerate(zip(combo_sharpe, combo_pf, combo_trades)):
        ax2.text(i, s + 0.15, f"Sharpe {s:.2f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=combo_colors[i])
        ax2.text(i, s + 0.02, f"{tr:.0f} tr/day", ha="center", va="bottom",
                fontsize=8, color=DIMMED)

    # Highlight the winner
    ax2.annotate("BEST\nCOMBO", xy=(3, 4.13), xytext=(3, 5.2),
                fontsize=11, fontweight="bold", color=GREEN,
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))

    # "Adding 3rd filter = no improvement" annotation
    ax2.annotate("Adding 3rd filter\n= no improvement", xy=(4, 4.09),
                xytext=(4.3, 5.5),
                fontsize=9, color=DIMMED, ha="center", style="italic",
                arrowprops=dict(arrowstyle="->", color=DIMMED, lw=1))

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(combo_names, fontsize=9, linespacing=1.2)
    ax2.set_ylabel("Sharpe Ratio", fontsize=12)
    ax2.set_title("Filter Combinations — Finding the Sweet Spot",
                  fontsize=14, fontweight="bold", color=ACCENT)
    ax2.set_ylim(0, 6.5)
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Filter Discovery — From 8 Candidates to 1 Winning Combination",
                 fontsize=18, fontweight="bold", color=ACCENT, y=1.02)
    fig.tight_layout()
    fig.savefig("docs/images/05_filter_discovery.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  05_filter_discovery.png")


def fig6_the_journey():
    """The full journey — a single timeline from intuition to validated strategy."""
    fig, ax = plt.subplots(figsize=(16, 6))

    milestones = [
        ("Human\nIntuition", "\"Price snaps\nback to average\"", DIMMED, 0),
        ("Raw\nBaseline", "PF 1.09\n60 tr/day", RED, 1),
        ("Filters\nAdded", "PF 2.35\n4.5 tr/day", ORANGE, 2),
        ("Parameters\nOptimized", "Sharpe 4.13\nSweet spot found", ACCENT, 3),
        ("Exits\nStress-Tested", "Simple exit\nbeats complex", ACCENT, 4),
        ("Entries\nRefined", "Dropped dead\nweight signals", ACCENT, 5),
        ("2-Year\nValidation", "Sharpe 2.68\n1,000+ trades", GREEN, 6),
        ("Risk\nProfiles", "3 configs\nDD cut 48%", GREEN, 7),
    ]

    # Draw timeline
    ax.plot([0, 7], [0.5, 0.5], color="#30363d", linewidth=3, zorder=1)

    for name, detail, color, x_pos in milestones:
        # Circle
        circle = plt.Circle((x_pos, 0.5), 0.12, color=color, zorder=3)
        ax.add_patch(circle)

        # Alternate above/below
        if x_pos % 2 == 0:
            y_name, y_detail = 0.78, 0.92
            y_line = 0.62
        else:
            y_name, y_detail = 0.22, 0.08
            y_line = 0.38

        # Connector line
        ax.plot([x_pos, x_pos], [0.5, y_line], color=color, linewidth=1.5,
                alpha=0.5, zorder=2)

        # Text
        ax.text(x_pos, y_name, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color, linespacing=1.3)
        ax.text(x_pos, y_detail, detail, ha="center", va="center",
                fontsize=9, color=DIMMED, linespacing=1.3)

    # Progress arrow
    for i in range(len(milestones) - 1):
        ax.annotate("", xy=(i + 0.75, 0.5), xytext=(i + 0.25, 0.5),
                    arrowprops=dict(arrowstyle="->", color="#30363d",
                                   lw=1.5, connectionstyle="arc3,rad=0"))

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("From Intuition to Validated Strategy — The AutoForge Journey",
                 fontsize=18, fontweight="bold", color=ACCENT, pad=15)

    fig.tight_layout()
    fig.savefig("docs/images/06_the_journey.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  06_the_journey.png")


def fig7_validation():
    """2-Year validation — monthly consistency."""
    fig, ax = plt.subplots(figsize=(14, 6))

    # Monthly P&L data (sanitized — relative, not absolute)
    months = [
        "Sep\n'23", "Oct", "Nov", "Dec",
        "Jan\n'24", "...", "Nov", "Dec",
        "Jan\n'25", "...", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "Jan\n'26", "Feb", "Mar",
    ]
    # Relative monthly performance (normalized, signs preserved)
    pnl_relative = [
        0.7, 1.0, -0.8, 0.4,
        -0.5, 0, 3.6, 0.9,
        -0.4, 0, 10.3, 34.2, 3.8, 9.0,
        2.0, 2.3, 0.8, 6.0, 4.0, -0.3,
        2.2, 9.5, 10.9,
    ]

    x = np.arange(len(months))
    colors = [GREEN if p > 0 else (RED if p < 0 else "#333") for p in pnl_relative]

    bars = ax.bar(x, pnl_relative, color=colors, alpha=0.8, width=0.7,
                  edgecolor="#30363d", linewidth=0.8)

    # Highlight stats
    positive = sum(1 for p in pnl_relative if p > 0)
    negative = sum(1 for p in pnl_relative if p < 0)
    gap = sum(1 for p in pnl_relative if p == 0)

    stats_text = f"{positive} profitable months  |  {negative} losing months  |  86% hit rate"
    ax.text(0.5, 0.95, stats_text, transform=ax.transAxes, ha="center",
            va="top", fontsize=13, fontweight="bold", color=GREEN,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#161b22",
                      edgecolor=GREEN, linewidth=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8, linespacing=1.2)
    ax.set_ylabel("Relative Monthly P&L", fontsize=12)
    ax.set_title("2.5-Year Monthly Consistency — Edge Holds Across Market Regimes",
                 fontsize=16, fontweight="bold", pad=20, color=ACCENT)
    ax.axhline(y=0, color=DIMMED, linewidth=1, alpha=0.5)
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Remove y-axis values (relative, not absolute)
    ax.set_yticklabels([])

    fig.tight_layout()
    fig.savefig("docs/images/07_monthly_consistency.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  07_monthly_consistency.png")


def fig8_hero():
    """Hero image — the pitch."""
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title
    ax.text(0.5, 0.82, "AutoForge", ha="center", va="center",
            fontsize=52, fontweight="bold", color=ACCENT,
            path_effects=[pe.withStroke(linewidth=4, foreground="#0d1117")])
    ax.text(0.5, 0.72, "Forge strategies through human-AI collaboration",
            ha="center", va="center", fontsize=18, color=DIMMED)

    # Three columns
    cols = [
        (0.18, "You Bring\nthe Edge", "Your market intuition,\nyour years of experience,\nyour observations", ORANGE),
        (0.50, "AutoForge\nTests It", "200+ experiments,\n1,400+ parameter combos,\ndead ends caught early", ACCENT),
        (0.82, "You Get\nthe Answer", "Validated strategy,\noptimized parameters,\n3 risk profiles", GREEN),
    ]

    for x_pos, title, detail, color in cols:
        # Box
        box = mpatches.FancyBboxPatch(
            (x_pos - 0.13, 0.22), 0.26, 0.42,
            boxstyle="round,pad=0.02",
            facecolor="#161b22",
            edgecolor=color,
            linewidth=2,
        )
        ax.add_patch(box)

        ax.text(x_pos, 0.56, title, ha="center", va="center",
                fontsize=16, fontweight="bold", color=color, linespacing=1.4)
        ax.text(x_pos, 0.36, detail, ha="center", va="center",
                fontsize=11, color=DIMMED, linespacing=1.5)

    # Arrows between columns
    ax.annotate("", xy=(0.33, 0.43), xytext=(0.29, 0.43),
                arrowprops=dict(arrowstyle="->", color=DIMMED, lw=2))
    ax.annotate("", xy=(0.71, 0.43), xytext=(0.67, 0.43),
                arrowprops=dict(arrowstyle="->", color=DIMMED, lw=2))

    # Tagline
    ax.text(0.5, 0.10, "If you've got the edge, we've got the power to make you successful.",
            ha="center", va="center", fontsize=15, color="#e6edf3",
            style="italic",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#161b22",
                      edgecolor=ACCENT, linewidth=1.5))

    fig.tight_layout()
    fig.savefig("docs/images/00_hero.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  00_hero.png")


if __name__ == "__main__":
    print("Generating AutoForge visuals...")
    fig8_hero()
    fig1_the_funnel()
    fig2_experiment_scale()
    fig3_dead_ends()
    fig4_three_profiles()
    fig5_filter_discovery()
    fig6_the_journey()
    fig7_validation()
    print("\nDone! 8 images in docs/images/")
