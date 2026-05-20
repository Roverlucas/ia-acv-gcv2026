"""Regional differentiation analysis.

For each call with non-null estimates for all three geographic scopes
(global, brazil, state), compute:

  1. Differentiates? (binary) — does the model return >3 distinct values?
     Threshold: distinct if pairwise relative difference >= 1%.
  2. Monotonic direction correct?
     Expected: global < brazil < state (for milk system in any BR state).
  3. State/Global ratio: LLM_ratio vs GT_ratio. Reported as log10 difference.
  4. Brazil/Global ratio: same.

Reads: results/processed/runs_long.csv (already produced by src/analyze.py)
  + per-system ground_truth.json (for system-specific GT ratios).

Writes:
  results/processed/regional_differentiation.csv
  results/processed/regional_summary.md
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "results" / "processed"
DATA_PROC = ROOT / "data" / "processed"

DIFF_THRESHOLD = 0.01  # 1% pairwise relative diff


def load_runs() -> pd.DataFrame:
    """Load the wide-format runs.csv produced by analyze.py."""
    p = PROC / "runs.csv"
    if not p.exists():
        raise FileNotFoundError("Run src/analyze.py first")
    df = pd.read_csv(p)
    return df


def load_gt(system: int) -> dict:
    """Return GT dict {global, brazil, state} for the given system."""
    p = DATA_PROC / f"s{system}" / "ground_truth.json"
    if not p.exists():
        # Fallback to S1 legacy file
        if system == 1:
            return {
                "global":   2.8297479606833848e-08,
                "brazil":   8.107650880339056e-08,
                "state":    6.37272783215278e-07,
            }
        raise FileNotFoundError(f"Missing GT for system {system}")
    data = json.loads(p.read_text(encoding="utf-8"))
    gt = data["ground_truth_economic"]
    # Older S1 schema may have 'state_sp' instead of 'state'
    if "state" not in gt and "state_sp" in gt:
        gt["state"] = gt["state_sp"]
    return gt


def classify_call(row: pd.Series, gt: dict) -> dict:
    """Classify a single call's regional differentiation."""
    # The wide df has v_global, v_brazil, v_state_sp (legacy) or v_state.
    # Accept both.
    g = row.get("v_global")
    b = row.get("v_brazil")
    s = row.get("v_state_sp") if "v_state_sp" in row else row.get("v_state")
    if s is None or pd.isna(s):
        s = row.get("v_state")
    vals = [g, b, s]
    if any(v is None or (isinstance(v, float) and np.isnan(v)) for v in vals):
        return {
            "responded_all": False, "differentiates": None,
            "monotonic": None, "ratio_state_global": None,
            "log10_ratio_diff_state_global": None,
            "ratio_brazil_global": None,
        }
    g, b, s = float(g), float(b), float(s)
    # Differentiation: any pairwise rel diff >= threshold
    def diff(a, c):
        return abs(a - c) / max(abs(a), abs(c)) if max(abs(a), abs(c)) > 0 else 0
    differentiates = (diff(g, b) >= DIFF_THRESHOLD
                      or diff(b, s) >= DIFF_THRESHOLD
                      or diff(g, s) >= DIFF_THRESHOLD)
    # Monotonic direction (global <= brazil <= state, expected for milk-system case)
    monotonic = (g <= b <= s)
    # Ratios
    rsg = s / g if g else None
    rbg = b / g if g else None
    rsg_gt = gt["state"] / gt["global"]
    log10_diff_rsg = np.log10(rsg / rsg_gt) if rsg and rsg_gt else None

    return {
        "responded_all": True,
        "differentiates": bool(differentiates),
        "monotonic": bool(monotonic),
        "ratio_state_global": rsg,
        "ratio_brazil_global": rbg,
        "ratio_state_global_gt": rsg_gt,
        "log10_ratio_diff_state_global": log10_diff_rsg,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    df = load_runs()
    # Determine system per call: from 'system' column if present, else from source_file
    if "system" not in df.columns:
        # All early runs were S1
        def detect_sys(src: str) -> int:
            if "s2_main" in src or "s2_stress" in src:
                return 2
            return 1
        df["system"] = df["source_file"].apply(detect_sys)

    # Compute per-call regional classification
    records = []
    for _, row in df.iterrows():
        gt = load_gt(int(row["system"]))
        cls = classify_call(row, gt)
        rec = {
            "system": int(row["system"]),
            "provider": row["provider"],
            "level": row["level"],
            "language": row["language"],
            "rep": row["rep"],
            **cls,
        }
        records.append(rec)
    out = pd.DataFrame(records)
    PROC.mkdir(parents=True, exist_ok=True)
    out.to_csv(PROC / "regional_differentiation.csv", index=False)
    print(f"Wrote {len(out)} call-level rows to regional_differentiation.csv")

    # Aggregate by (system × provider × level)
    sub = out[out["responded_all"]]
    agg = (sub.groupby(["system", "provider", "level"])
              .agg(n=("responded_all", "size"),
                   share_differentiates=("differentiates", "mean"),
                   share_monotonic=("monotonic", "mean"),
                   median_ratio_state_global=("ratio_state_global", "median"),
                   median_log10_ratio_diff=("log10_ratio_diff_state_global", "median"))
              .reset_index())

    print("\n=== Regional differentiation by (system × LLM × level) ===")
    print(agg.round(3).to_string(index=False))

    # Markdown summary
    md_lines = ["# Regional differentiation analysis\n\n"]
    md_lines.append("## Criteria\n")
    md_lines.append("- **Differentiates**: pairwise relative difference between scopes >= 1% in at least one pair.\n")
    md_lines.append("- **Monotonic**: global <= brazil <= state (expected for milk-system regionalization).\n")
    md_lines.append("- **State/Global ratio**: ratio reported by LLM vs published GT.\n\n")
    md_lines.append("## Aggregated results\n\n")
    md_lines.append(agg.round(3).to_markdown(index=False))
    (PROC / "regional_summary.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nWrote regional_summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
