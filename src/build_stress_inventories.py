"""Generate perturbed inventories + new ground truths for the stress test.

Three perturbations of Sistema 1 (Oberschelp, economic allocation):
- P1 (scale):  todas as massas × 2.0
- P2 (NH3):    massa de Ammonia × 0.1, demais inalteradas
- P3 (random): cada substância × U[0.5, 2.0] com seed=42

Writes:
  data/processed/stress/lci_P{1,2,3}.md            (LCI table for prompt injection)
  data/processed/stress/gt_P{1,2,3}.json           (new ground truth)
  data/processed/stress/cf_oberschelp_s1.md        (CFs unchanged, copied for self-contained input)
"""

from __future__ import annotations
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
OUT = PROC / "stress"
OUT.mkdir(parents=True, exist_ok=True)

# Load base LCI and CFs
with open(PROC / "sistema1_emissions_air.json") as f:
    lci = json.load(f)
with open(PROC / "cf_oberschelp_s1.json") as f:
    cfs = json.load(f)

# Group fluxes by substance (aggregated mass)
agg_masses = {}
for r in lci["pm_relevant_flows"]:
    agg_masses.setdefault(r["substance"], 0.0)
    agg_masses[r["substance"]] += r["value"]

# Per-flow perturbation factors based on substance family
def perturbation_factor(substance: str, scheme: str, rng: random.Random) -> float:
    if scheme == "P1":
        return 2.0
    if scheme == "P2":
        return 0.1 if substance == "Ammonia" else 1.0
    if scheme == "P3":
        # Stable per-substance factor (so each LLM call sees the same numbers)
        return rng.uniform(0.5, 2.0)
    raise ValueError(scheme)


def write_markdown_table(rows: list[dict], path: Path) -> None:
    md = "| Substância | Compartimento | Quantidade (kg / kg FPCM) |\n|---|---|---|\n"
    for r in rows:
        md += f"| {r['substance']} | {r['compartment']} | {r['value']:.4e} |\n"
    path.write_text(md, encoding="utf-8")


def gt_for_scheme(scheme: str) -> tuple[dict, dict, list[dict]]:
    """Compute new GT + perturbed total masses + per-row perturbed table."""
    rng = random.Random(42)
    perturbed_rows = []
    new_masses_by_substance = {}
    for r in lci["pm_relevant_flows"]:
        f = perturbation_factor(r["substance"], scheme, rng)
        new_val = r["value"] * f
        perturbed_rows.append({
            "substance": r["substance"],
            "compartment": r["compartment"],
            "value": new_val,
        })
        new_masses_by_substance.setdefault(r["substance"], 0.0)
        new_masses_by_substance[r["substance"]] += new_val

    # New GT = sum over substances of new_mass × CF
    new_gt = {"global": 0.0, "brazil": 0.0, "state_sp": 0.0}
    breakdown = {}
    for sub, m_new in new_masses_by_substance.items():
        if sub not in cfs["cfs"]:
            continue  # only PM precursors with CFs contribute to impact
        cf = cfs["cfs"][sub]["cf_daly_per_kg"]
        breakdown[sub] = {
            "new_mass_total": m_new,
            "cf_global": cf["global"],
            "cf_brazil": cf["brazil"],
            "cf_state_sp": cf["state_sp"],
        }
        for k in new_gt:
            new_gt[k] += m_new * cf[k]

    return new_gt, breakdown, perturbed_rows


def main() -> int:
    schemes = ["P1", "P2", "P3"]
    summary = {}
    original_gt = {
        "global":   2.8297479606833848e-08,
        "brazil":   8.107650880339056e-08,
        "state_sp": 6.37272783215278e-07,
    }
    for s in schemes:
        gt, breakdown, rows = gt_for_scheme(s)
        write_markdown_table(rows, OUT / f"lci_{s}.md")
        out = {
            "scheme": s,
            "description": {
                "P1": "all masses x 2.0",
                "P2": "Ammonia x 0.1, others unchanged",
                "P3": "each substance x U[0.5, 2.0], seed=42",
            }[s],
            "original_ground_truth": original_gt,
            "new_ground_truth": gt,
            "ratio_new_over_original": {k: gt[k] / original_gt[k] for k in gt},
            "breakdown_by_substance": breakdown,
        }
        with open(OUT / f"gt_{s}.json", "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        summary[s] = {
            "new_gt_global": gt["global"],
            "ratio_global": gt["global"] / original_gt["global"],
        }
        print(f"{s}: new GT global = {gt['global']:.3e} (×{gt['global']/original_gt['global']:.3f} vs original)")

    # Also copy the CF table (unchanged) so each prompt is self-contained
    cf_md_source = PROC / "cf_oberschelp_s1.md"
    (OUT / "cf_oberschelp_s1.md").write_text(cf_md_source.read_text(encoding="utf-8"), encoding="utf-8")

    print("\nFiles written to data/processed/stress/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
