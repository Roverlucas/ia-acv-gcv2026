"""Generate figures for the GCV 2026 extended abstract.

Reads: results/processed/runs_long.parquet
Writes:
  - results/figures/fig1_mape_vs_level.pdf|png
  - results/figures/fig2_log_ratio_box.pdf|png
  - results/figures/fig3_char_model_choice.pdf|png
  - results/figures/fig4_agreement_share.pdf|png
"""

from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "results" / "processed"
FIGS = ROOT / "results" / "figures"

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "figure.dpi": 150,
})

LEVEL_ORDER = ["L0", "L1", "L2", "L3", "L4"]
PROVIDERS = ["gpt", "gemini", "deepseek"]
PROVIDER_COLORS = {
    "gpt": "#10A37F",
    "gemini": "#4285F4",
    "deepseek": "#E63946",
}
PROVIDER_LABELS = {"gpt": "GPT", "gemini": "Gemini", "deepseek": "DeepSeek"}


def load_long() -> pd.DataFrame:
    p = PROC / "runs_long.parquet"
    if not p.exists():
        raise FileNotFoundError(f"Run src/analyze.py first to produce {p}")
    df = pd.read_parquet(p)
    df["level"] = pd.Categorical(df["level"], categories=LEVEL_ORDER, ordered=True)
    return df


# --------- Fig 1: MAPE vs level (3 LLMs × 2 langs) ---------
def fig1_mape_vs_level(long: pd.DataFrame, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), sharey=True)
    for ax, lang in zip(axes, ["pt-BR", "en"]):
        sub = long[long["language"] == lang]
        for prov in PROVIDERS:
            x_vals, y_med, y_lo, y_hi = [], [], [], []
            for lvl in LEVEL_ORDER:
                vals = sub[(sub["provider"] == prov) & (sub["level"] == lvl)]["abs_rel_error"].dropna().values
                if len(vals) == 0:
                    continue
                x_vals.append(lvl)
                y_med.append(np.median(vals))
                y_lo.append(np.percentile(vals, 25))
                y_hi.append(np.percentile(vals, 75))
            if not x_vals:
                continue
            ax.plot(x_vals, y_med, marker="o", color=PROVIDER_COLORS[prov], label=PROVIDER_LABELS[prov], linewidth=1.6)
            ax.fill_between(x_vals, y_lo, y_hi, alpha=0.15, color=PROVIDER_COLORS[prov])
        ax.set_yscale("log")
        ax.set_title(lang)
        ax.set_xlabel("Nível de enriquecimento de prompt")
        ax.axhline(0.30, color="black", linestyle=":", linewidth=0.8, alpha=0.6)
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("Erro relativo absoluto (mediana, IQR)")
    axes[0].legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


# --------- Fig 2: log10(estimate / GT) distribution ---------
def fig2_log_ratio_box(long: pd.DataFrame, out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), sharey=True)
    for ax, lang in zip(axes, ["pt-BR", "en"]):
        sub = long[long["language"] == lang]
        positions = []
        data = []
        colors = []
        labels = []
        i = 0
        for lvl in LEVEL_ORDER:
            for prov in PROVIDERS:
                vals = sub[(sub["provider"] == prov) & (sub["level"] == lvl)]["log_ratio"].dropna().values
                if len(vals) == 0:
                    continue
                data.append(vals)
                positions.append(i)
                colors.append(PROVIDER_COLORS[prov])
                labels.append(f"{lvl}/{PROVIDER_LABELS[prov]}")
                i += 1
            i += 0.5
        bp = ax.boxplot(data, positions=positions, widths=0.7, patch_artist=True,
                        flierprops=dict(marker=".", markersize=3))
        for patch, c in zip(bp["boxes"], colors):
            patch.set_facecolor(c)
            patch.set_alpha(0.6)
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=70, ha="right", fontsize=6)
        ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
        ax.set_title(lang)
        ax.grid(True, alpha=0.3, axis="y")
    axes[0].set_ylabel("log₁₀(estimativa / GT)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


# --------- Fig 3: characterization model choice by level (stacked bars) ---------
def fig3_char_model_choice(long: pd.DataFrame, out: Path) -> None:
    # 1 row per call (collapse geo_scope by keeping first)
    df = long.drop_duplicates(["provider", "level", "language", "rep"])
    fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    for ax, lang in zip(axes, ["pt-BR", "en"]):
        sub = df[df["language"] == lang]
        tab = (sub.groupby(["level", "characterization_model_class"]).size()
                  .unstack(fill_value=0)
                  .reindex(LEVEL_ORDER))
        share = tab.div(tab.sum(axis=1), axis=0)
        share.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", width=0.8)
        ax.set_ylabel("Fração das respostas")
        ax.set_title(f"Modelo de caracterização declarado por nível — {lang}")
        ax.legend(title="Modelo", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=7)
        ax.set_xlabel("")
    axes[-1].set_xlabel("Nível de enriquecimento")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


# --------- Fig 4: share of estimates within 30% of GT ---------
def fig4_agreement_share(long: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    summary = (long.groupby(["provider", "level", "language"])["within_30pct"]
                   .mean()
                   .reset_index())
    width = 0.13
    x = np.arange(len(LEVEL_ORDER))
    offsets = {("gpt", "pt-BR"): -2.5, ("gpt", "en"): -1.5,
               ("gemini", "pt-BR"): -0.5, ("gemini", "en"): 0.5,
               ("deepseek", "pt-BR"): 1.5, ("deepseek", "en"): 2.5}
    for (prov, lang), off in offsets.items():
        sub = summary[(summary["provider"] == prov) & (summary["language"] == lang)]
        sub = sub.set_index("level").reindex(LEVEL_ORDER)
        c = PROVIDER_COLORS[prov]
        hatch = "//" if lang == "en" else None
        ax.bar(x + off * width, sub["within_30pct"], width=width, color=c,
               hatch=hatch, edgecolor="white", linewidth=0.5,
               label=f"{PROVIDER_LABELS[prov]} {lang}")
    ax.set_xticks(x)
    ax.set_xticklabels(LEVEL_ORDER)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Fração de estimativas com erro < 30%")
    ax.set_xlabel("Nível de enriquecimento de prompt")
    ax.set_title("Concordância operacional vs. ground truth (3 escopos × 5 repetições)")
    ax.legend(loc="upper left", frameon=False, ncol=3, fontsize=7)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    FIGS.mkdir(parents=True, exist_ok=True)
    long = load_long()
    print(f"Loaded {len(long)} (call × geo_scope) rows.")

    print("Generating Fig 1 (MAPE × level)...")
    fig1_mape_vs_level(long, FIGS / "fig1_mape_vs_level")
    print("Generating Fig 2 (log ratio box)...")
    fig2_log_ratio_box(long, FIGS / "fig2_log_ratio_box")
    print("Generating Fig 3 (model choice)...")
    fig3_char_model_choice(long, FIGS / "fig3_char_model_choice")
    print("Generating Fig 4 (agreement share)...")
    fig4_agreement_share(long, FIGS / "fig4_agreement_share")
    print(f"Done. Figures in {FIGS}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
