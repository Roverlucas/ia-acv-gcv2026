"""Generate supplementary tables (LaTeX fragments) for the SM.

Writes to manuscript/gcv2026/supplementary/tables/sm_*.tex
"""

from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "results" / "processed"
SM_TABLES = ROOT / "manuscript" / "gcv2026" / "supplementary" / "tables"
SM_TABLES.mkdir(parents=True, exist_ok=True)

PROVIDERS_ORDER = ["gpt", "gemini", "deepseek"]
PROVIDER_LABELS = {"gpt": "GPT", "gemini": "Gemini", "deepseek": "DeepSeek"}
LEVELS = ["L0", "L1", "L2", "L3", "L4"]


def fmt_pct(x):
    if pd.isna(x):
        return "---"
    if abs(x) >= 1:
        return f"$+{x:.1f}\\times$"
    return f"{x*100:+.0f}\\%"


def fmt_e(x):
    if pd.isna(x):
        return "---"
    return f"${x:.2e}$".replace("e", r" \times 10^{").replace("e-", r"\times 10^{-") + "}"


def fmt_simple(x, dec=2):
    if pd.isna(x):
        return "---"
    return f"{x:.{dec}f}"


def fmt_br(x, dec=2):
    """Decimal comma, as used in the running text of the manuscript (PT-BR)."""
    if pd.isna(x):
        return "---"
    return f"{x:.{dec}f}".replace(".", ",")


def mape_by_geo_long(long: pd.DataFrame) -> str:
    """One table per system: MAPE by (LLM × level × idioma × escopo)."""
    out = []
    for sys_n in [1, 2]:
        sub = long[long["system"] == sys_n]
        # Mean abs_rel_error
        agg = (sub.groupby(["provider", "level", "language", "geo_scope"])
                  ["abs_rel_error"].mean()
                  .unstack("geo_scope")
                  .reindex(columns=["global", "brazil", "state"]))
        lines = []
        lines.append(r"\begin{table}[h]")
        lines.append(r"\centering")
        lines.append(r"\small")
        lines.append(rf"\caption{{S{sys_n}. Erro relativo absoluto m\'edio (MAPE) por (LLM $\times$ n\'ivel $\times$ idioma $\times$ escopo geogr\'afico) --- Sistema {sys_n}.}}")
        lines.append(rf"\label{{tab:sm_mape_s{sys_n}}}")
        lines.append(r"\begin{tabular}{llccc}")
        lines.append(r"\toprule")
        lines.append(r"\textbf{LLM} & \textbf{Nivel / Idioma} & \textbf{Global} & \textbf{Brasil} & \textbf{Estado} \\")
        lines.append(r"\midrule")
        for prov in PROVIDERS_ORDER:
            for lvl in LEVELS:
                for lang in ["pt-BR", "en"]:
                    key = (prov, lvl, lang)
                    if key not in agg.index:
                        continue
                    row = agg.loc[key]
                    cells = [fmt_pct(row.get("global")), fmt_pct(row.get("brazil")), fmt_pct(row.get("state"))]
                    lines.append(f"{PROVIDER_LABELS[prov]} & {lvl} / {lang} & " + " & ".join(cells) + r" \\")
            lines.append(r"\midrule")
        # Remove last \midrule
        if lines[-1].strip() == r"\midrule":
            lines.pop()
        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")
        out.append("\n".join(lines))
    return "\n\n".join(out)


def cv_intra_cell(long: pd.DataFrame) -> str:
    """Intra-cell CV (variability among 5 reps) by (system × LLM × level × idioma × escopo)."""
    cv = (long.groupby(["system", "provider", "level", "language", "geo_scope"])["estimate"]
              .apply(lambda x: np.nanstd(x) / np.nanmean(x) if np.nanmean(x) and len(x.dropna()) > 1 else np.nan)
              .reset_index(name="cv"))
    # Pivot: rows = (system, provider, level), cols = (language)
    pv = (cv.groupby(["system", "provider", "level", "language"])["cv"].mean()
            .unstack("language").round(3))
    lines = [r"\begin{table}[h]", r"\centering", r"\small",
             r"\caption{Coeficiente de varia\c{c}\~ao intra-c\'elula (CV entre 5 repeti\c{c}\~oes), m\'edia sobre 3 escopos geogr\'aficos.}",
             r"\label{tab:sm_cv}",
             r"\begin{tabular}{cllcc}",
             r"\toprule",
             r"\textbf{Sis.} & \textbf{LLM} & \textbf{Nivel} & \textbf{CV (PT-BR)} & \textbf{CV (EN)} \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        for prov in PROVIDERS_ORDER:
            for lvl in LEVELS:
                key = (sys_n, prov, lvl)
                if key not in pv.index:
                    continue
                row = pv.loc[key]
                lines.append(f"S{sys_n} & {PROVIDER_LABELS[prov]} & {lvl} & {fmt_simple(row.get('pt-BR'), 3)} & {fmt_simple(row.get('en'), 3)} \\\\")
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def stress_classification(stress_files: list[Path]) -> str:
    """Full classification of all 180 stress test calls."""
    rows = []
    for f in stress_files:
        # Default system from filename ("s2_stress" -> 2, else 1)
        default_sys = 2 if "s2_stress" in f.name else 1
        with open(f) as fh:
            for line in fh:
                r = json.loads(line)
                sys_n = r.get("system", default_sys)
                p = r.get("parsed_output") or r.get("parsed_output_lenient") or {}
                ans_g = (p.get("answer") or {}).get("global", {}).get("value")
                new_gt = r["new_ground_truth"]["global"]
                orig_gt = r["original_ground_truth"]["global"]
                if isinstance(ans_g, (int, float)):
                    e_new = abs((ans_g - new_gt) / new_gt)
                    e_orig = abs((ans_g - orig_gt) / orig_gt)
                    if e_new < 0.10:
                        cls = "calc"
                    elif e_orig < 0.10:
                        cls = "mem"
                    else:
                        cls = "misto"
                else:
                    cls = "null"
                rows.append({
                    "system": sys_n, "provider": r["provider"],
                    "level": r["level"], "scheme": r["scheme"], "class": cls
                })
    df = pd.DataFrame(rows)
    ct = (df.groupby(["system", "provider", "scheme", "level", "class"]).size()
            .unstack("class", fill_value=0)
            .reindex(columns=["calc", "mem", "misto", "null"], fill_value=0))
    lines = [r"\begin{table}[h]", r"\centering", r"\small",
             r"\caption{Classifica\c{c}\~ao detalhada das 180 chamadas do teste de contamina\c{c}\~ao por (sistema $\times$ LLM $\times$ esquema $\times$ n\'ivel). Cada c\'elula tem $n=5$ chamadas.}",
             r"\label{tab:sm_stress_detail}",
             r"\begin{tabular}{ccllcccc}",
             r"\toprule",
             r"\textbf{Sis.} & \textbf{LLM} & \textbf{Esquema} & \textbf{Nivel} & \textbf{C\'alc.} & \textbf{Mem.} & \textbf{Misto} & \textbf{Null} \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        for prov in PROVIDERS_ORDER:
            for scheme in ["P1", "P2", "P3"]:
                for lvl in ["L3", "L4"]:
                    key = (sys_n, prov, scheme, lvl)
                    if key not in ct.index:
                        continue
                    row = ct.loc[key]
                    lines.append(f"S{sys_n} & {PROVIDER_LABELS[prov]} & {scheme} & {lvl} & "
                                 f"{int(row['calc'])} & {int(row['mem'])} & {int(row['misto'])} & {int(row['null'])} \\\\")
            lines.append(r"\midrule")
        if lines[-1].strip() == r"\midrule":
            lines.pop()
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def stress_gt_ratio() -> str:
    """Effect of each perturbation scheme on the ground truth.

    Reads the recomputed GTs written by build_stress_inventories.py and reports
    new GT / original GT per (system x scheme x geographic scope). Demonstrates
    that every scheme displaces the recomputed GT far enough from the published
    value for the calculo/memorizacao classes to be disjoint.
    """
    stress_dir = ROOT / "data" / "processed"
    scopes = ["global", "brazil", "state"]
    rows = []
    for sys_n in [1, 2]:
        for scheme in ["P1", "P2", "P3"]:
            path = stress_dir / f"s{sys_n}" / "stress" / f"gt_{scheme}.json"
            d = json.loads(path.read_text(encoding="utf-8"))
            rows.append({
                "system": sys_n,
                "scheme": scheme,
                **{s: d["ratio_new_over_original"][s] for s in scopes},
            })

    # Smallest displacement from the published value across all cells; the
    # classification threshold is 10%, so this must stay comfortably above it.
    min_departure = min(abs(r[s] - 1.0) for r in rows for s in scopes)

    lines = [r"\begin{table}[h]", r"\centering", r"\small",
             r"\caption{Efeito de cada esquema de perturba\c{c}\~ao sobre o \emph{ground truth}: "
             r"raz\~ao entre o GT recalculado a partir do invent\'ario perturbado e o GT original "
             r"publicado, por sistema e escopo geogr\'afico.}",
             r"\label{tab:sm_stress_gt_ratio}",
             r"\begin{tabular}{clccc}",
             r"\toprule",
             r"& & \multicolumn{3}{c}{\textbf{GT novo / GT original}} \\",
             r"\cmidrule(lr){3-5}",
             r"\textbf{Sis.} & \textbf{Esquema} & \textbf{Global} & \textbf{Brasil} & \textbf{Estado} \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        for r in [x for x in rows if x["system"] == sys_n]:
            cells = " & ".join(fmt_br(r[s], 3) for s in scopes)
            lines.append(f"S{sys_n} & {r['scheme']} & {cells} \\\\")
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption*{\footnotesize Nota: raz\~ao $1{,}000$ indicaria aus\^encia de deslocamento. "
              r"O P1 desloca proporcionalmente e de forma id\^entica nos tr\^es escopos; o P2 desloca de "
              r"forma distinta por escopo, porque o fator de caracteriza\c{c}\~ao da am\^onia \'e "
              r"regionalizado; o P3 desloca sem padr\~ao. O menor deslocamento observado entre as 18 "
              rf"c\'elulas \'e de {fmt_br(min_departure*100, 1)}\%, acima do limiar de $\pm 10\%$ usado na "
              r"classifica\c{c}\~ao, de modo que nenhuma chamada pode "
              r"satisfazer simultaneamente os crit\'erios de \emph{c\'alculo} e de \emph{memoriza\c{c}\~ao}. "
              r"Fonte: autores.}",
              r"\end{table}"]
    return "\n".join(lines)


def regional_ratios(long: pd.DataFrame) -> str:
    """Median state/global ratio per (system, LLM, level)."""
    # Compute state/global per call
    wide = (long.pivot_table(index=["system", "provider", "level", "language", "rep"],
                              columns="geo_scope", values="estimate")
                  .reset_index())
    wide["ratio_sg"] = wide["state"] / wide["global"]
    med = (wide.groupby(["system", "provider", "level"])["ratio_sg"]
                .median().reset_index())
    pv = med.pivot(index=["system", "provider"], columns="level", values="ratio_sg").reindex(columns=LEVELS).round(2)
    gt_ratios = {1: 22.52, 2: 12.13}
    lines = [r"\begin{table}[h]", r"\centering", r"\small",
             r"\caption{Raz\~ao mediana \emph{Estado/Global} reportada pelos LLMs vs. \emph{ground truth} publicado.}",
             r"\label{tab:sm_regional}",
             r"\begin{tabular}{clccccc l}",
             r"\toprule",
             r"\textbf{Sis.} & \textbf{LLM} & \textbf{L0} & \textbf{L1} & \textbf{L2} & \textbf{L3} & \textbf{L4} & \textbf{GT publicado} \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        for prov in PROVIDERS_ORDER:
            key = (sys_n, prov)
            if key not in pv.index:
                continue
            row = pv.loc[key]
            cells = [fmt_simple(row.get(lv), 2) for lv in LEVELS]
            lines.append(f"S{sys_n} & {PROVIDER_LABELS[prov]} & " + " & ".join(cells) + f" & {gt_ratios[sys_n]:.2f}" + r" \\")
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def char_model_choice_per_system(runs: pd.DataFrame) -> str:
    """Char model choice frequency by (system × level)."""
    # Deduplicate per call (geo_scope expansion in long), use unique provider/level/lang/rep
    df = runs.copy()
    df = df.drop_duplicates(["system", "provider", "level", "language", "rep"])
    crosstab = (df.groupby(["system", "level", "characterization_model_class"]).size()
                  .unstack(fill_value=0))
    cols = ["oberschelp", "recipe", "impact_world", "fantke", "other", "unspecified"]
    cols = [c for c in cols if c in crosstab.columns]
    crosstab = crosstab.reindex(columns=cols, fill_value=0)
    pretty = {"oberschelp": "Oberschelp", "recipe": "ReCiPe 2016",
              "impact_world": "IMPACT World+", "fantke": "Fantke",
              "other": "Outro", "unspecified": "N\~ao espec."}
    lines = [r"\begin{table}[h]", r"\centering", r"\small",
             r"\caption{Modelo de caracteriza\c{c}\~ao declarado pelos LLMs por (sistema $\times$ n\'ivel). Conta-se PT-BR + EN.}",
             r"\label{tab:sm_char_choice}",
             r"\begin{tabular}{cl" + "c" * len(cols) + "}",
             r"\toprule",
             r"\textbf{Sis.} & \textbf{Nivel} & " + " & ".join(f"\\textbf{{{pretty[c]}}}" for c in cols) + r" \\",
             r"\midrule"]
    for sys_n in [1, 2]:
        for lvl in LEVELS:
            key = (sys_n, lvl)
            if key not in crosstab.index:
                continue
            row = crosstab.loc[key]
            lines.append(f"S{sys_n} & {lvl} & " + " & ".join(str(int(v)) for v in row.values) + r" \\")
        lines.append(r"\midrule")
    if lines[-1].strip() == r"\midrule":
        lines.pop()
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def main() -> int:
    long = pd.read_csv(PROC / "runs_long.csv")
    runs = pd.read_csv(PROC / "runs.csv")

    (SM_TABLES / "sm_mape_by_geo.tex").write_text(mape_by_geo_long(long), encoding="utf-8")
    (SM_TABLES / "sm_cv.tex").write_text(cv_intra_cell(long), encoding="utf-8")
    (SM_TABLES / "sm_regional.tex").write_text(regional_ratios(long), encoding="utf-8")
    (SM_TABLES / "sm_char_choice.tex").write_text(char_model_choice_per_system(runs), encoding="utf-8")

    stress_files = sorted((ROOT / "results" / "raw").glob("*stress*.jsonl"))
    (SM_TABLES / "sm_stress_detail.tex").write_text(stress_classification(stress_files), encoding="utf-8")
    (SM_TABLES / "sm_stress_gt_ratio.tex").write_text(stress_gt_ratio(), encoding="utf-8")

    print(f"Wrote 6 SM table fragments to {SM_TABLES}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
