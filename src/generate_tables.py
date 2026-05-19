"""Generate LaTeX table fragments from analysis output.

Reads: results/processed/runs_long.parquet
Writes: manuscript/gcv2026/tables/*.tex (fragments to \input{} from main .tex)
"""

from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LONG_PATH = ROOT / "results" / "processed" / "runs_long.parquet"
RUNS_PATH = ROOT / "results" / "processed" / "runs.parquet"
OUT_DIR = ROOT / "manuscript" / "gcv2026" / "tables"

LEVEL_ORDER = ["L0", "L1", "L2", "L3", "L4"]
PROVIDER_ORDER = ["gpt", "gemini", "deepseek"]
PROVIDER_LABELS = {"gpt": "GPT", "gemini": "Gemini", "deepseek": "DeepSeek"}
LANG_LABELS = {"pt-BR": "PT-BR", "en": "EN"}


def fmt_pct(x: float) -> str:
    if pd.isna(x):
        return "---"
    if x >= 10:
        return f"{x:.0f}\\times"  # show as N× when extreme
    return f"{x*100:.0f}\\%"


def fmt_rel(x: float) -> str:
    """Format relative error: % under 100%, ×N over 100%."""
    if pd.isna(x):
        return "---"
    if abs(x) < 1.0:
        return f"{x*100:+.0f}\\%"
    return f"{x:+.1f}\\times"


def tbl_summary_mape(long: pd.DataFrame) -> str:
    """Table: MAPE by (LLM × language × level), averaged over geo & reps."""
    grp = (long.groupby(["provider", "language", "level"])["abs_rel_error"]
                .mean()
                .reset_index()
                .rename(columns={"abs_rel_error": "mape"}))
    pivot = grp.pivot_table(index=["provider", "language"], columns="level", values="mape")
    pivot = pivot.reindex(columns=LEVEL_ORDER)

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\caption{MAPE por LLM $\times$ idioma $\times$ nível (média sobre 3 escopos $\times$ 5 reps).}")
    lines.append(r"\label{tab:summary}")
    lines.append(r"\begin{tabular}{llccccc}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{LLM} & \textbf{Idioma} & \textbf{L0} & \textbf{L1} & \textbf{L2} & \textbf{L3} & \textbf{L4} \\")
    lines.append(r"\midrule")
    for prov in PROVIDER_ORDER:
        for lang in ["pt-BR", "en"]:
            key = (prov, lang)
            if key not in pivot.index:
                continue
            row = pivot.loc[key]
            cells = [fmt_rel(v) for v in row.values]
            lines.append(f"{PROVIDER_LABELS[prov]} & {LANG_LABELS[lang]} & " + " & ".join(cells) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption*{\footnotesize Erro relativo absoluto médio (MAPE). Valores apresentados em \% até 100\%; acima disso, em múltiplos do GT ($\times$).}")
    lines.append(r"\end{table}")
    return "\n".join(lines)


def tbl_char_model_choice(long: pd.DataFrame) -> str:
    """Table: characterization model class chosen by level (PT-BR)."""
    df = long.drop_duplicates(["provider", "level", "language", "rep"])
    df = df[df["language"] == "pt-BR"]
    crosstab = (df.groupby(["level", "characterization_model_class"]).size()
                  .unstack(fill_value=0)
                  .reindex(LEVEL_ORDER, fill_value=0))
    cols = ["oberschelp", "recipe", "impact_world", "fantke", "other", "unspecified"]
    cols = [c for c in cols if c in crosstab.columns]
    crosstab = crosstab[cols]

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\caption{Modelo de caracterização declarado pelas LLMs por nível (PT-BR, contagem agregada).}")
    lines.append(r"\label{tab:charmodel}")
    lines.append(r"\begin{tabular}{l" + "c" * len(cols) + "}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Nível} & " + " & ".join(f"\\textbf{{{c.replace('_',' ').title()}}}" for c in cols) + r" \\")
    lines.append(r"\midrule")
    for lvl in LEVEL_ORDER:
        row = crosstab.loc[lvl]
        lines.append(f"{lvl} & " + " & ".join(str(int(v)) for v in row.values) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    return "\n".join(lines)


def tbl_agreement(long: pd.DataFrame) -> str:
    """Table: share of estimates with abs_rel_error < 30%."""
    grp = (long.groupby(["provider", "language", "level"])["within_30pct"]
                .mean()
                .reset_index())
    pivot = grp.pivot_table(index=["provider", "language"], columns="level", values="within_30pct")
    pivot = pivot.reindex(columns=LEVEL_ORDER)

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\caption{Fração de estimativas com erro relativo absoluto $<30\%$ (critério operacional de concordância).}")
    lines.append(r"\label{tab:agreement}")
    lines.append(r"\begin{tabular}{llccccc}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{LLM} & \textbf{Idioma} & \textbf{L0} & \textbf{L1} & \textbf{L2} & \textbf{L3} & \textbf{L4} \\")
    lines.append(r"\midrule")
    for prov in PROVIDER_ORDER:
        for lang in ["pt-BR", "en"]:
            key = (prov, lang)
            if key not in pivot.index:
                continue
            row = pivot.loc[key]
            cells = [f"{v*100:.0f}\\%" if pd.notna(v) else "---" for v in row.values]
            lines.append(f"{PROVIDER_LABELS[prov]} & {LANG_LABELS[lang]} & " + " & ".join(cells) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    if not LONG_PATH.exists():
        print(f"Missing {LONG_PATH}. Run src/analyze.py first.")
        return 1

    long = pd.read_parquet(LONG_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    (OUT_DIR / "tbl_summary.tex").write_text(tbl_summary_mape(long), encoding="utf-8")
    (OUT_DIR / "tbl_charmodel.tex").write_text(tbl_char_model_choice(long), encoding="utf-8")
    (OUT_DIR / "tbl_agreement.tex").write_text(tbl_agreement(long), encoding="utf-8")

    print(f"Wrote 3 table fragments to {OUT_DIR}/")
    print("  tbl_summary.tex      MAPE × LLM × lang × level")
    print("  tbl_charmodel.tex    Model choice frequency by level (PT-BR)")
    print("  tbl_agreement.tex    Share within 30% by LLM × lang × level")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
