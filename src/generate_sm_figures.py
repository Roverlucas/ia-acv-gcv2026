"""Generate supplementary figures for the SM.

Writes PDFs and PNGs to manuscript/gcv2026/supplementary/figures/
"""

from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "results" / "processed"
SM_FIGS = ROOT / "manuscript" / "gcv2026" / "supplementary" / "figures"
SM_FIGS.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "figure.dpi": 150,
})

PROVIDER_ORDER = ["gpt", "gemini", "deepseek"]
PROVIDER_COLORS = {"gpt": "#10A37F", "gemini": "#4285F4", "deepseek": "#E63946"}
PROVIDER_LABELS = {"gpt": "GPT", "gemini": "Gemini", "deepseek": "DeepSeek"}
LEVEL_ORDER = ["L0", "L1", "L2", "L3", "L4"]


def fig_mape_by_system(long: pd.DataFrame, out: Path) -> None:
    """Figure: MAPE curves separated by system (2 panels)."""
    long = long.copy()
    long["level"] = pd.Categorical(long["level"], categories=LEVEL_ORDER, ordered=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, sys_n in zip(axes, [1, 2]):
        sub = long[(long["system"] == sys_n) & (long["language"] == "pt-BR")]
        for prov in PROVIDER_ORDER:
            xs, ys_med, ys_lo, ys_hi = [], [], [], []
            for lvl in LEVEL_ORDER:
                vals = sub[(sub["provider"] == prov) & (sub["level"] == lvl)]["abs_rel_error"].dropna().values
                if not len(vals):
                    continue
                xs.append(lvl)
                ys_med.append(np.median(vals))
                ys_lo.append(np.percentile(vals, 25))
                ys_hi.append(np.percentile(vals, 75))
            if not xs:
                continue
            ax.plot(xs, ys_med, marker="o", color=PROVIDER_COLORS[prov],
                    label=PROVIDER_LABELS[prov], linewidth=1.6)
            ax.fill_between(xs, ys_lo, ys_hi, alpha=0.15, color=PROVIDER_COLORS[prov])
        ax.set_yscale("log")
        ax.set_title(f"Sistema {sys_n}")
        ax.set_xlabel("Nível de enriquecimento de prompt")
        ax.axhline(0.30, color="black", linestyle=":", linewidth=0.8, alpha=0.6)
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("Erro relativo absoluto (mediana, IQR)")
    axes[0].legend(loc="upper right", frameon=False)
    fig.suptitle("Curva de saturação MAPE × nível por sistema (PT-BR)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_log_ratio_by_level(long: pd.DataFrame, out: Path) -> None:
    """Distribution of log10(estimate/GT) per level."""
    long = long.copy()
    long["level"] = pd.Categorical(long["level"], categories=LEVEL_ORDER, ordered=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, sys_n in zip(axes, [1, 2]):
        sub = long[long["system"] == sys_n]
        for i, prov in enumerate(PROVIDER_ORDER):
            for j, lvl in enumerate(LEVEL_ORDER):
                vals = sub[(sub["provider"] == prov) & (sub["level"] == lvl)]["log_ratio"].dropna().values
                if not len(vals):
                    continue
                pos = j * 4 + i
                bp = ax.boxplot(vals, positions=[pos], widths=0.6, patch_artist=True,
                                flierprops=dict(marker=".", markersize=3))
                bp["boxes"][0].set_facecolor(PROVIDER_COLORS[prov])
                bp["boxes"][0].set_alpha(0.6)
        ax.set_title(f"Sistema {sys_n}")
        ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
        ax.set_xticks([1 + j * 4 for j in range(5)])
        ax.set_xticklabels(LEVEL_ORDER)
        ax.grid(True, alpha=0.3, axis="y")
    axes[0].set_ylabel(r"$\log_{10}(\hat{I}/I_{\mathrm{GT}})$")
    # Legend
    handles = [plt.Rectangle((0, 0), 1, 1, fc=PROVIDER_COLORS[p], alpha=0.6, label=PROVIDER_LABELS[p])
               for p in PROVIDER_ORDER]
    axes[1].legend(handles=handles, loc="upper right", frameon=False)
    fig.suptitle("Distribuição da log-razão (estimativa/GT) por sistema, LLM e nível")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_stress_scatter(stress_files: list[Path], out: Path) -> None:
    """Scatter: response vs new GT (color by class), per scheme."""
    rows = []
    for f in stress_files:
        default_sys = 2 if "s2_stress" in f.name else 1
        with open(f) as fh:
            for line in fh:
                r = json.loads(line)
                p = r.get("parsed_output") or r.get("parsed_output_lenient") or {}
                ans = (p.get("answer") or {}).get("global", {}).get("value")
                if not isinstance(ans, (int, float)):
                    continue
                rows.append({
                    "system": r.get("system", default_sys),
                    "provider": r["provider"], "scheme": r["scheme"],
                    "ans": ans, "new_gt": r["new_ground_truth"]["global"],
                    "orig_gt": r["original_ground_truth"]["global"],
                })
    df = pd.DataFrame(rows)
    fig, axes = plt.subplots(2, 3, figsize=(11, 6), sharex=False, sharey=False)
    for i, sys_n in enumerate([1, 2]):
        for j, scheme in enumerate(["P1", "P2", "P3"]):
            ax = axes[i, j]
            sub = df[(df["system"] == sys_n) & (df["scheme"] == scheme)]
            for prov in PROVIDER_ORDER:
                psub = sub[sub["provider"] == prov]
                ax.scatter(psub["new_gt"], psub["ans"], color=PROVIDER_COLORS[prov],
                           alpha=0.55, s=24, label=PROVIDER_LABELS[prov], edgecolor="white", linewidth=0.5)
            if len(sub):
                orig = sub["orig_gt"].iloc[0]
                new_gt = sub["new_gt"].iloc[0]
                ax.axhline(orig, color="black", linestyle=":", linewidth=0.7, label="GT original" if (i, j) == (0, 0) else None)
                ax.axhline(new_gt, color="gray", linestyle="--", linewidth=0.7, label="Novo GT" if (i, j) == (0, 0) else None)
            ax.set_title(f"Sistema {sys_n} · {scheme}")
            ax.set_yscale("log")
            ax.set_xscale("log")
            ax.grid(True, alpha=0.3, which="both")
            if i == 1:
                ax.set_xlabel("Novo GT (DALY/kg FPCM)")
            if j == 0:
                ax.set_ylabel("Resposta do LLM (DALY/kg FPCM)")
    axes[0, 0].legend(loc="lower right", frameon=False, fontsize=7)
    fig.suptitle("Teste de contaminação: respostas dos LLMs vs novo ground truth (escopo Global)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_cv_heatmap(long: pd.DataFrame, out: Path) -> None:
    """Heatmap of intra-cell CV (LLM × level × system)."""
    cv = (long.groupby(["system", "provider", "level", "language", "geo_scope"])["estimate"]
              .apply(lambda x: np.nanstd(x) / np.nanmean(x) if np.nanmean(x) and len(x.dropna()) > 1 else np.nan)
              .reset_index(name="cv"))
    mean_cv = cv.groupby(["system", "provider", "level"])["cv"].mean().reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
    for ax, sys_n in zip(axes, [1, 2]):
        sub = mean_cv[mean_cv["system"] == sys_n]
        pivot = sub.pivot(index="provider", columns="level", values="cv").reindex(index=PROVIDER_ORDER, columns=LEVEL_ORDER)
        im = ax.imshow(pivot.values, cmap="viridis_r", aspect="auto", vmin=0, vmax=1.5)
        ax.set_xticks(range(len(LEVEL_ORDER)))
        ax.set_xticklabels(LEVEL_ORDER)
        ax.set_yticks(range(len(PROVIDER_ORDER)))
        ax.set_yticklabels([PROVIDER_LABELS[p] for p in PROVIDER_ORDER])
        ax.set_title(f"Sistema {sys_n}")
        for i_p, prov in enumerate(PROVIDER_ORDER):
            for j_l, lvl in enumerate(LEVEL_ORDER):
                val = pivot.loc[prov, lvl] if lvl in pivot.columns and prov in pivot.index else np.nan
                if pd.notna(val):
                    ax.text(j_l, i_p, f"{val:.2f}", ha="center", va="center",
                            color="white" if val > 0.5 else "black", fontsize=8)
    fig.colorbar(im, ax=axes, fraction=0.03, pad=0.04, label="CV intra-célula")
    fig.suptitle("Coeficiente de variação entre 5 repetições (T=0)")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    long = pd.read_csv(PROC / "runs_long.csv")
    print("Generating SM Fig 1 (MAPE × level per system)...")
    fig_mape_by_system(long, SM_FIGS / "sm_fig1_mape_by_system")
    print("Generating SM Fig 2 (log ratio distribution)...")
    fig_log_ratio_by_level(long, SM_FIGS / "sm_fig2_log_ratio")
    print("Generating SM Fig 3 (stress scatter)...")
    stress_files = sorted((ROOT / "results" / "raw").glob("*stress*.jsonl"))
    fig_stress_scatter(stress_files, SM_FIGS / "sm_fig3_stress_scatter")
    print("Generating SM Fig 4 (CV heatmap)...")
    fig_cv_heatmap(long, SM_FIGS / "sm_fig4_cv_heatmap")
    print(f"\nDone. Saved 4 figures to {SM_FIGS}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
