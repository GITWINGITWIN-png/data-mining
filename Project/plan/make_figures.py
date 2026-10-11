"""Generate the figures for the group work-plan document (plan/group_plan.tex).

Every chart and every number the plan quotes about the premise test comes from
the files the pipeline already writes:

* ``04_Evaluation/premise_test/results/alg1_results.json`` — flagged share of
  volume per window and per threshold θ (Algorithm 1)
* ``04_Evaluation/premise_test/results/extract_stats.json`` — row counts before
  and after pre-processing
* ``04_Evaluation/premise_test/results/dec2024_top_wash_markets.csv`` — the
  markets that carry the most flagged volume in the Dec-2024 week

If the pipeline is re-run and these files change, re-run this script and
re-check the numbers written in the prose of the plan.

Run (from Project/):  uv run python plan/make_figures.py
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "04_Evaluation" / "premise_test" / "results"
OUT = HERE / "figures"

# Same hues as the \definecolor block in group_plan.tex, so a colour means the
# same thing in the prose, the diagrams and the charts (Okabe–Ito, colour-blind safe).
C_DATA = "#0072B2"  # blue   — data pipeline (person A) / the peak window
C_ALG = "#D55E00"  # orange — Algorithm 1 (person B)
C_EVAL = "#009E73"  # green  — evaluation / the quiet window
C_EXT = "#7B5EA7"  # purple — EDA + chip dumping (person C)
C_INK = "#1A2733"
C_MUTED = "#5B6B7A"

plt.rcParams.update({
    "figure.dpi": 150,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.6,
    "axes.edgecolor": C_MUTED,
    "axes.labelcolor": C_INK,
    "text.color": C_INK,
    "xtick.color": C_MUTED,
    "ytick.color": C_MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 9,
})


def theta_sensitivity(res: dict) -> None:
    """Flagged share of volume vs θ, peak week against quiet week."""
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    for key, label, color in [
        ("dec2024", "Dec 1-7, 2024 (peak)", C_DATA),
        ("jun2025", "Jun 1-7, 2025 (quiet)", C_EVAL),
    ]:
        by = res[key]["wash_fraction_by_theta"]
        th = [float(t) for t in by]
        frac = [100 * v for v in by.values()]
        ax.plot(th, frac, marker="o", color=color, lw=1.8, label=label)
        # label the point at the threshold we actually use
        f09 = 100 * res[key]["wash_fraction_theta_0.9"]
        ax.annotate(f"{f09:.2f}%" if f09 < 1 else f"{f09:.1f}%", (0.9, f09),
                    textcoords="offset points", xytext=(6, 6), color=color, fontsize=8.5,
                    fontweight="bold")

    # go / no-go rule written before the test was run
    ax.axhspan(30, 100, color=C_DATA, alpha=0.06, lw=0)
    ax.axhspan(0, 10, color=C_EVAL, alpha=0.08, lw=0)
    ax.axhline(30, color=C_DATA, lw=0.8, ls=":")
    ax.axhline(10, color=C_EVAL, lw=0.8, ls=":")
    ax.text(0.702, 31.5, "GO needs peak >= 30%", color=C_DATA, fontsize=7.5)
    ax.text(0.815, 11.5, "GO needs quiet <= 10%", color=C_EVAL, fontsize=7.5)
    ax.axvline(0.9, color=C_ALG, lw=1, ls="--")
    ax.text(0.902, 92, "theta = 0.9", color=C_ALG, fontsize=7.5)

    ax.set_xlim(0.69, 1.0)
    ax.set_ylim(0, 100)
    ax.set_xlabel("threshold theta (both wallets must score >= theta)")
    ax.set_ylabel("flagged share of week's volume (%)")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(0.0, 0.58))
    fig.tight_layout()
    fig.savefig(OUT / "theta_sensitivity.png")
    plt.close(fig)


def top_markets(df: pd.DataFrame) -> None:
    """Which markets carry the flagged volume in the peak week."""
    df = df.iloc[::-1]  # largest on top
    names = [n if len(n) <= 48 else n[:46] + "..." for n in df["market_name"]]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    colors = [C_ALG if "Trump" in n else C_DATA for n in names]
    ax.barh(names, df["wash_Mshares"], color=colors, height=0.65)
    for y, (v, f) in enumerate(zip(df["wash_Mshares"], df["frac_in_market"])):
        ax.text(v + 0.4, y, f"{100 * f:.0f}% of market", va="center", fontsize=7, color=C_MUTED)
    ax.set_xlabel("flagged volume, Dec 1-7 2024 (million shares)")
    ax.set_xlim(0, df["wash_Mshares"].max() * 1.32)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "top_markets.png")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    res = json.loads((RESULTS / "alg1_results.json").read_text())
    theta_sensitivity(res)
    top_markets(pd.read_csv(RESULTS / "dec2024_top_wash_markets.csv"))
    print("figures written to", OUT)


if __name__ == "__main__":
    main()
