"""Analyze experimental results — compute MAPE, log-MAPE, CV, agreement metrics.

Usage:
    python src/analyze.py                          # processa todos os JSONL em results/raw/
    python src/analyze.py --input results/raw/<file>.jsonl
    python src/analyze.py --gt-only                # apenas check de cross-validation contra GT

Outputs:
    results/processed/runs.parquet         # 1 linha por chamada
    results/processed/aggregated.csv       # 1 linha por (provider × level × lang × geo)
    results/processed/summary.md           # tabela markdown resumida
"""

from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "results" / "raw"
PROC_DIR = ROOT / "results" / "processed"

GROUND_TRUTH_BY_SYSTEM = {
    1: {"global": 2.8297479606833848e-08,
        "brazil": 8.107650880339056e-08,
        "state":  6.37272783215278e-07},
    2: {"global": 1.2811260424359784e-08,
        "brazil": 1.0956135102805530e-07,
        "state":  1.5536479051332848e-07},
}

# -----------------------------------------------------------------
# Loading
# -----------------------------------------------------------------
def load_jsonl(path: Path) -> list[dict]:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def discover_files(input_arg: str | None) -> list[Path]:
    if input_arg:
        p = Path(input_arg)
        return [p] if p.is_file() else sorted(p.glob("*.jsonl"))
    return sorted(RAW_DIR.glob("*.jsonl"))


# -----------------------------------------------------------------
# Categorize free-text fields
# -----------------------------------------------------------------
def classify_char_model(text: str | None) -> str:
    if not text or text.lower() in {"unspecified", "n/a", "none"}:
        return "unspecified"
    t = text.lower()
    if "oberschelp" in t: return "oberschelp"
    if "fantke" in t: return "fantke"
    if "van zelm" in t or "vanzelm" in t: return "van_zelm"
    if "tang" in t and ("2018" in t or "lca" in t or "lime" in t): return "tang"
    if "recipe" in t or "recipe" in t.replace(" ", "") or "frischknecht" in t or "jolliet" in t: return "recipe"
    if "impact world" in t or "impactworld" in t: return "impact_world"
    if "useetox" in t or "usetox" in t: return "usetox"
    if "ilcd" in t: return "ilcd"
    if "ef 3" in t or "ef3" in t: return "ef"
    return "other"


def classify_alloc(text: str | None) -> str:
    if not text:
        return "unspecified"
    t = text.lower().strip()
    if "econ" in t: return "economic"
    if "mass" in t and "econ" not in t: return "mass"
    if "system" in t or "expansion" in t: return "system_expansion"
    if t == "none": return "none"
    if t in {"unspecified", "other"}: return t
    return "other"


# -----------------------------------------------------------------
# Per-call extraction
# -----------------------------------------------------------------
def extract_record(run: dict, source_file: str) -> dict:
    parsed = run.get("parsed_output") or run.get("parsed_output_lenient")
    resp = run.get("response") or {}
    err = resp.get("error")
    parse_err = run.get("parse_error")
    lenient_recovered = bool(run.get("lenient_recovered"))

    answer = (parsed or {}).get("answer") or {}
    g = (answer.get("global") or {}).get("value")
    b = (answer.get("brazil") or {}).get("value")
    # Schema changed mid-experiment: state_sp (legacy S1) -> state (generic).
    s = ((answer.get("state") or {}).get("value")
         if "state" in answer else (answer.get("state_sp") or {}).get("value"))

    def num_or_none(x):
        return float(x) if isinstance(x, (int, float)) else None

    g, b, s = num_or_none(g), num_or_none(b), num_or_none(s)

    char_model = (parsed or {}).get("characterization_model")
    alloc = (parsed or {}).get("allocation_method")
    confidence = (parsed or {}).get("confidence")
    refs = (parsed or {}).get("references") or []
    n_refs = len(refs) if isinstance(refs, list) else 0

    return {
        "source_file": source_file,
        "provider": run.get("provider"),
        "model_id": run.get("model_id"),
        "level": run.get("level"),
        "language": run.get("language"),
        "rep": run.get("rep"),
        "temperature": run.get("temperature"),
        "prompt_hash": run.get("prompt_hash"),
        "v_global": g,
        "v_brazil": b,
        "v_state": s,
        # Determine system from the run record itself or from filename
        "system": run.get("system") or (2 if "s2" in source_file else 1),
        "characterization_model_raw": char_model,
        "characterization_model_class": classify_char_model(char_model),
        "allocation_method_raw": alloc,
        "allocation_method_class": classify_alloc(alloc),
        "confidence": confidence,
        "n_references": n_refs,
        "json_strict_ok": run.get("parsed_output") is not None,
        "json_lenient_recovered": lenient_recovered,
        "api_error": err,
        "input_tokens": resp.get("input_tokens"),
        "output_tokens": resp.get("output_tokens"),
        "cost_usd": resp.get("cost_usd"),
        "elapsed_s": resp.get("elapsed_s"),
        "timestamp_utc": resp.get("timestamp_utc"),
    }


def build_runs_df(files: Iterable[Path]) -> pd.DataFrame:
    records = []
    for f in files:
        for run in load_jsonl(f):
            records.append(extract_record(run, f.name))
    df = pd.DataFrame(records)
    return df


# -----------------------------------------------------------------
# Per-scope long format and metrics
# -----------------------------------------------------------------
def to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Long-format: one row per (call × geo scope)."""
    long = df.melt(
        id_vars=[c for c in df.columns if not c.startswith("v_")],
        value_vars=["v_global", "v_brazil", "v_state"],
        var_name="geo_scope",
        value_name="estimate",
    )
    long["geo_scope"] = long["geo_scope"].str.replace("v_", "")
    # Per-row GT depends on system
    def _gt(row):
        return GROUND_TRUTH_BY_SYSTEM.get(int(row["system"]), {}).get(row["geo_scope"], np.nan)
    long["ground_truth"] = long.apply(_gt, axis=1)
    long["abs_error"] = (long["estimate"] - long["ground_truth"]).abs()
    long["rel_error"] = (long["estimate"] - long["ground_truth"]) / long["ground_truth"]
    long["abs_rel_error"] = long["rel_error"].abs()
    long["log_ratio"] = np.where(
        long["estimate"] > 0,
        np.log10(long["estimate"] / long["ground_truth"]),
        np.nan,
    )
    long["responded"] = long["estimate"].notna()
    long["within_30pct"] = long["abs_rel_error"] < 0.30
    return long


def aggregate(long: pd.DataFrame) -> pd.DataFrame:
    """Aggregate by (system × provider × level × language × geo_scope)."""
    grp = long.groupby(
        ["system", "provider", "level", "language", "geo_scope"], dropna=False
    )
    agg = grp.agg(
        n_total=("estimate", "size"),
        n_responded=("responded", "sum"),
        mape=("abs_rel_error", "mean"),
        median_abs_rel_error=("abs_rel_error", "median"),
        median_log_ratio=("log_ratio", "median"),
        cv_estimate=("estimate", lambda x: (np.nanstd(x) / np.nanmean(x)) if np.nanmean(x) else np.nan),
        share_within_30=("within_30pct", "mean"),
    ).reset_index()
    return agg


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--exclude-smoke", action="store_true",
                        help="ignore JSONL files containing 'smoke' in name")
    args = parser.parse_args()

    files = discover_files(args.input)
    if args.exclude_smoke:
        files = [f for f in files if "smoke" not in f.name]
    if not files:
        print("No JSONL files found.")
        return 1

    print(f"Loading {len(files)} file(s):")
    for f in files:
        print(f"  - {f.name}")

    df = build_runs_df(files)
    print(f"\nTotal calls: {len(df)}")
    print(df.groupby(["provider", "level", "language"]).size().unstack(fill_value=0))

    long = to_long(df)
    agg = aggregate(long)

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROC_DIR / "runs.csv", index=False)
    long.to_csv(PROC_DIR / "runs_long.csv", index=False)
    agg.to_csv(PROC_DIR / "aggregated.csv", index=False)

    # Print summary table
    print("\n=== AGGREGATED MAPE BY (SYSTEM, LLM, LEVEL, LANG) — mean over 3 geo scopes & reps ===")
    pivot = (long.groupby(["system", "provider", "level", "language"])["abs_rel_error"]
                  .mean()
                  .unstack("language")
                  .round(3))
    print(pivot)

    # Save markdown summary
    md_lines = ["# Aggregated results\n\n"]
    md_lines.append("## MAPE by (LLM × level × language)\n\n")
    md_lines.append(pivot.to_markdown())
    md_lines.append("\n\n## Aggregated table\n\n")
    md_lines.append(agg.round(4).to_markdown(index=False))
    (PROC_DIR / "summary.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nSaved: runs.parquet, runs_long.parquet, aggregated.csv, summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
