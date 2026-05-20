"""Generate comparative tables/figures: Giusti et al. vs LLM responses.

Outputs:
  - manuscript/gcv2026/supplementary/tables/sm_comparative.tex
  - manuscript/gcv2026/supplementary/tables/sm_threshold_sensitivity.tex
  - manuscript/gcv2026/supplementary/tables/sm_stress_by_perturbation.tex
  - manuscript/gcv2026/supplementary/figures/sm_fig5_giusti_vs_llm.{pdf,png}
"""

from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "results" / "processed"
SM_TABLES = ROOT / "manuscript" / "gcv2026" / "supplementary" / "tables"
SM_FIGS = ROOT / "manuscript" / "gcv2026" / "supplementary" / "figures"
SM_TABLES.mkdir(parents=True, exist_ok=True)
SM_FIGS.mkdir(parents=True, exist_ok=True)

PROVIDER_ORDER = ["gpt", "gemini", "deepseek"]
PROVIDER_LABELS = {"gpt": "GPT-4.1", "gemini": "Gemini 2.5 Pro", "deepseek": "DeepSeek V3"}
PROVIDER_COLORS = {"gpt": "#10A37F", "gemini": "#4285F4", "deepseek": "#E63946"}

GT = {
    1: {"global": 2.8297e-08, "brazil": 8.1077e-08, "state": 6.3727e-07, "state_label": "SP"},
    2: {"global": 1.2811e-08, "brazil": 1.0956e-07, "state": 1.5536e-07, "state_label": "PR"},
}

mpl.rcParams.update({"font.family": "serif", "font.size": 9, "figure.dpi": 150})


def fmt_sci(x):
    if x is None or pd.isna(x):
        return "---"
    mantissa, exponent = f"{x:.2e}".split("e")
    exp_int = int(exponent)
    return f"${mantissa} \\times 10^{{{exp_int}}}$"


def cp_ci(k, n, alpha=0.05):
    lo = beta.ppf(alpha / 2, k, n - k + 1) if k > 0 else 0.0
    hi = beta.ppf(1 - alpha / 2, k + 1, n - k) if k < n else 1.0
    return lo, hi


# -----------------------------------------------------------------
# 1. Comparative table: Giusti vs LLM median (L3 + L4, PT-BR)
# -----------------------------------------------------------------
def comparative_giusti_vs_llm(long: pd.DataFrame) -> str:
    sub = long[(long["language"] == "pt-BR") & (long["level"].isin(["L3", "L4"]))]
    med = (sub.groupby(["system", "provider", "geo_scope"])["estimate"].median().reset_index())
    lines = [r"\begin{table}[h]", r"\centering", r"\footnotesize",
             r"\caption{Comparação entre o \emph{ground truth} de Giusti \emph{et al.} (2023) e a mediana das respostas dos LLMs em L3+L4 (PT-BR, $n=10$ por célula). Valores em DALY/kg FPCM.}",
             r"\label{tab:sm_comparative}",
             r"\begin{tabular}{l l c c c}",
             r"\toprule",
             r"\textbf{Sistema} & \textbf{LLM / fonte} & \textbf{Global} & \textbf{Brasil} & \textbf{Estado} \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        gt = GT[sys_n]
        lines.append(f"S{sys_n} ({gt['state_label']}) & \\textit{{Giusti et al. (2023)}} & "
                     f"{fmt_sci(gt['global'])} & {fmt_sci(gt['brazil'])} & {fmt_sci(gt['state'])} \\\\")
        for prov in PROVIDER_ORDER:
            row = med[(med["system"] == sys_n) & (med["provider"] == prov)]
            g = row[row["geo_scope"] == "global"]["estimate"].values
            b = row[row["geo_scope"] == "brazil"]["estimate"].values
            s = row[row["geo_scope"] == "state"]["estimate"].values
            gv = g[0] if len(g) and not pd.isna(g[0]) else None
            bv = b[0] if len(b) and not pd.isna(b[0]) else None
            sv = s[0] if len(s) and not pd.isna(s[0]) else None
            lines.append(f" & {PROVIDER_LABELS[prov]} & {fmt_sci(gv)} & {fmt_sci(bv)} & {fmt_sci(sv)} \\\\")
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


# -----------------------------------------------------------------
# 2. Threshold sensitivity (10% vs 5% vs 15%)
# -----------------------------------------------------------------
def threshold_sensitivity(stress_files: list[Path]) -> str:
    runs = []
    for f in stress_files:
        default_sys = 2 if "s2_stress" in f.name else 1
        with open(f) as fh:
            for line in fh:
                r = json.loads(line)
                p = r.get("parsed_output") or r.get("parsed_output_lenient") or {}
                ans = (p.get("answer") or {}).get("global", {}).get("value")
                if isinstance(ans, (int, float)):
                    new_gt = r["new_ground_truth"]["global"]
                    orig_gt = r["original_ground_truth"]["global"]
                    runs.append({
                        "system": r.get("system", default_sys),
                        "provider": r["provider"],
                        "e_new": abs((ans - new_gt) / new_gt),
                        "e_orig": abs((ans - orig_gt) / orig_gt),
                    })
    df = pd.DataFrame(runs)
    lines = [r"\begin{table}[h]", r"\centering", r"\footnotesize",
             r"\caption{Sensibilidade da classificação à escolha do limiar (taxa de \emph{memorização} em \% para diferentes janelas).}",
             r"\label{tab:sm_threshold}",
             r"\begin{tabular}{l c ccc ccc}",
             r"\toprule",
             r"& & \multicolumn{3}{c}{\textbf{Sistema 1}} & \multicolumn{3}{c}{\textbf{Sistema 2}} \\",
             r"\textbf{LLM} & $n$ & 5\% & 10\% & 15\% & 5\% & 10\% & 15\% \\",
             r"\midrule"]
    for prov in PROVIDER_ORDER:
        row = [PROVIDER_LABELS[prov], "30"]
        for sys_n in [1, 2]:
            sub = df[(df["provider"] == prov) & (df["system"] == sys_n)]
            for thr in [0.05, 0.10, 0.15]:
                n = len(sub)
                if n == 0:
                    row.append("---")
                    continue
                mem = (sub["e_orig"] < thr).sum()
                row.append(f"{mem/n*100:.0f}\\%")
        lines.append(" & ".join(row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


# -----------------------------------------------------------------
# 3. Stress breakdown by perturbation (P1/P2/P3) and level (L3/L4)
# -----------------------------------------------------------------
def stress_breakdown(stress_files: list[Path]) -> str:
    rows = []
    for f in stress_files:
        default_sys = 2 if "s2_stress" in f.name else 1
        with open(f) as fh:
            for line in fh:
                r = json.loads(line)
                p = r.get("parsed_output") or r.get("parsed_output_lenient") or {}
                ans = (p.get("answer") or {}).get("global", {}).get("value")
                if isinstance(ans, (int, float)):
                    new_gt = r["new_ground_truth"]["global"]
                    orig_gt = r["original_ground_truth"]["global"]
                    e_new = abs((ans - new_gt) / new_gt)
                    e_orig = abs((ans - orig_gt) / orig_gt)
                    cls = "calc" if e_new < 0.10 else ("mem" if e_orig < 0.10 else "mix")
                else:
                    cls = "null"
                rows.append({"system": r.get("system", default_sys),
                             "provider": r["provider"],
                             "scheme": r["scheme"], "level": r["level"], "class": cls})
    df = pd.DataFrame(rows)
    ct = df[df["class"] == "mem"].groupby(["system", "provider", "scheme", "level"]).size()
    total = df.groupby(["system", "provider", "scheme", "level"]).size()
    rate = (ct / total).fillna(0).reset_index(name="rate")

    lines = [r"\begin{table}[h]", r"\centering", r"\footnotesize",
             r"\caption{Decomposição da taxa de \emph{memorização} por perturbação e por nível (chamadas/$5$ por célula).}",
             r"\label{tab:sm_stress_break}",
             r"\begin{tabular}{l l ccc ccc}",
             r"\toprule",
             r"& & \multicolumn{3}{c}{\textbf{L3}} & \multicolumn{3}{c}{\textbf{L4}} \\",
             r"\textbf{LLM} & \textbf{Sis.} & P1 & P2 & P3 & P1 & P2 & P3 \\",
             r"\midrule"]
    for prov in PROVIDER_ORDER:
        for sys_n in [1, 2]:
            cells = [PROVIDER_LABELS[prov], f"S{sys_n}"]
            for lvl in ["L3", "L4"]:
                for sch in ["P1", "P2", "P3"]:
                    rcell = rate[(rate["provider"] == prov) & (rate["system"] == sys_n) &
                                 (rate["scheme"] == sch) & (rate["level"] == lvl)]
                    if len(rcell):
                        cells.append(f"{rcell['rate'].iloc[0]*5:.0f}/5")
                    else:
                        cells.append("0/5")
            lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


# -----------------------------------------------------------------
# 4. Comparative figure: Giusti vs LLM
# -----------------------------------------------------------------
def fig_giusti_vs_llm(long: pd.DataFrame, out: Path) -> None:
    sub = long[(long["language"] == "pt-BR") & (long["level"].isin(["L3", "L4"]))]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=False)
    for ax, sys_n in zip(axes, [1, 2]):
        gt = GT[sys_n]
        scopes = ["global", "brazil", "state"]
        gt_vals = [gt[s] for s in scopes]
        x = np.arange(len(scopes))
        width = 0.18
        # Plot GT bars
        ax.bar(x - 2 * width, gt_vals, width, color="black", alpha=0.85,
               label=r"Giusti \emph{et al.} (2023)", edgecolor="white", linewidth=0.5)
        # LLM medians
        for i, prov in enumerate(PROVIDER_ORDER):
            psub = sub[(sub["system"] == sys_n) & (sub["provider"] == prov)]
            med = psub.groupby("geo_scope")["estimate"].median()
            vals = [med.get(s, np.nan) for s in scopes]
            ax.bar(x + (i - 1) * width, vals, width,
                   color=PROVIDER_COLORS[prov], alpha=0.85,
                   label=PROVIDER_LABELS[prov], edgecolor="white", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(["Global", "Brasil", f"Estado-{gt['state_label']}"])
        ax.set_yscale("log")
        ax.set_title(f"Sistema {sys_n} ({gt['state_label']})")
        ax.grid(True, alpha=0.3, axis="y", which="both")
        if sys_n == 1:
            ax.set_ylabel("Impacto (DALY/kg FPCM)")
    axes[0].legend(loc="upper left", frameon=False, fontsize=7.5)
    fig.suptitle("Ground truth publicado vs. mediana das respostas dos LLMs (L3+L4, PT-BR)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    long = pd.read_csv(PROC / "runs_long.csv")
    stress_files = sorted((ROOT / "results" / "raw").glob("*stress*.jsonl"))

    (SM_TABLES / "sm_comparative.tex").write_text(comparative_giusti_vs_llm(long), encoding="utf-8")
    (SM_TABLES / "sm_threshold_sensitivity.tex").write_text(threshold_sensitivity(stress_files), encoding="utf-8")
    (SM_TABLES / "sm_stress_by_perturbation.tex").write_text(stress_breakdown(stress_files), encoding="utf-8")
    fig_giusti_vs_llm(long, SM_FIGS / "sm_fig5_giusti_vs_llm")

    print("Wrote: sm_comparative, sm_threshold_sensitivity, sm_stress_by_perturbation, sm_fig5_giusti_vs_llm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
