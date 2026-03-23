"""Generate a terminal screenshot showing AutoForge in action."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams.update({
    "font.family": "monospace",
    "font.size": 11,
})

BG = "#1e1e2e"
FG = "#cdd6f4"
GREEN = "#a6e3a1"
BLUE = "#89b4fa"
YELLOW = "#f9e2af"
RED = "#f38ba8"
DIMMED = "#6c7086"
CYAN = "#94e2d5"
MAUVE = "#cba6f7"


def terminal():
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Terminal chrome
    title_bar = mpatches.FancyBboxPatch(
        (0.02, 0.955), 0.96, 0.035,
        boxstyle="round,pad=0.005",
        facecolor="#313244",
        edgecolor="#45475a",
        linewidth=1,
    )
    ax.add_patch(title_bar)

    # Window buttons
    for i, color in enumerate(["#f38ba8", "#f9e2af", "#a6e3a1"]):
        circle = plt.Circle((0.05 + i * 0.02, 0.9725), 0.006, color=color)
        ax.add_patch(circle)

    ax.text(0.5, 0.9725, "AutoForge — Parameter Sweep", ha="center", va="center",
            fontsize=10, color=DIMMED)

    # Terminal body
    body = mpatches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.935,
        boxstyle="round,pad=0.005",
        facecolor="#11111b",
        edgecolor="#45475a",
        linewidth=1,
    )
    ax.add_patch(body)

    lines = [
        (DIMMED,  "$ python examples/s5_reversion.py --data data/NQ_21range.csv --optimize --phase filters"),
        (FG,      ""),
        (BLUE,    "Loaded 524,757 bars from data/NQ_21range.csv"),
        (FG,      ""),
        (YELLOW,  "--- Phase: filters (160 combinations) ---"),
        (FG,      ""),
        (CYAN,    "AutoForge: sweeping 160 parameter combinations..."),
        (DIMMED,  "  ... 100/160 done"),
        (GREEN,   "AutoForge: sweep complete. Best net_pnl: $21,306.40"),
        (FG,      ""),
        (YELLOW,  "Top 10 by net_pnl:"),
        (DIMMED,  "─" * 85),
        (DIMMED,  "  trend_flt  ext_flt  trend_pd   ext_thr       net_pnl       sharpe    win_rate      trades       max_dd"),
        (DIMMED,  "─" * 85),
        (GREEN,   "      True     True        21        10    $21,306.40         4.13       73.8%          122   $2,483.00"),
        (FG,      "      True     True        21        12    $17,567.20         4.39       71.6%           81   $2,246.00"),
        (FG,      "      True     True        14        10    $19,882.00         3.76       72.1%          135   $2,891.00"),
        (FG,      "      True     True        30        10    $16,445.60         3.52       71.9%           98   $2,102.00"),
        (FG,      "      True     True        14        12    $15,211.80         3.89       73.2%           89   $1,988.00"),
        (FG,      "     False     True        21        10    $14,882.40         2.94       68.8%          197   $3,456.00"),
        (FG,      "      True    False        21        10    $12,106.00         2.53       69.5%          178   $3,211.00"),
        (FG,      "      True     True        30        12    $11,987.60         3.41       72.8%           67   $1,876.00"),
        (FG,      "     False     True        14        10    $11,540.20         2.67       67.2%          214   $3,892.00"),
        (FG,      "     False    False        21        10     $8,954.00         1.64       62.9%          412   $5,127.00"),
        (DIMMED,  "─" * 85),
        (FG,      ""),
        (GREEN,   "★ Best: trend_filter=True, extension_filter=True, period=21, threshold=10"),
        (GREEN,   "  Sharpe 4.13 | 73.8% win | PF 2.35 | $174.64/trade | MaxDD $2,483"),
        (FG,      ""),
        (DIMMED,  "$ "),
    ]

    y = 0.93
    line_height = 0.028
    for color, text in lines:
        if text == "":
            y -= line_height * 0.5
            continue
        # Truncate long lines
        display = text[:95]
        # Escape $ for matplotlib (it treats $ as math delimiter)
        display = display.replace("$", "\\$")
        ax.text(0.04, y, display, fontsize=8.5, color=color,
                fontfamily="monospace", va="top")
        y -= line_height

    fig.tight_layout(pad=0.5)
    fig.savefig("docs/images/08_terminal.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close()
    print("  08_terminal.png")


if __name__ == "__main__":
    terminal()
