"""Generate perturbed inventories + new ground truths for the stress test.

Three perturbations of Sistema N (Oberschelp, economic allocation):
- P1 (scale):  todas as massas × 2.0
- P2 (NH3):    massa de Ammonia × 0.1, demais inalteradas
- P3 (random): cada substância × U[0.5, 2.0] com seed=42

Usage:
    python src/build_stress_inventories.py --system 1
    python src/build_stress_inventories.py --system 2

Writes:
  data/processed/s{N}/stress/lci_P{1,2,3}.md
  data/processed/s{N}/stress/gt_P{1,2,3}.json
  data/processed/s{N}/stress/cf_oberschelp.md       (CFs unchanged, copied)
"""

from __future__ import annotations
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"


def load_system(system: int) -> tuple[dict, dict, dict]:
    """Load LCI, CFs, and ground truth for the given system."""
    sys_dir = PROC / f"s{system}"
    with open(sys_dir / "emissions_air.json") as f:
        lci = json.load(f)
    with open(sys_dir / "cf_oberschelp.json") as f:
        cfs = json.load(f)
    with open(sys_dir / "ground_truth.json") as f:
        gt = json.load(f)
    return lci, cfs, gt


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


def gt_for_scheme(scheme: str, lci: dict, cfs: dict) -> tuple[dict, dict, list[dict]]:
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

    new_gt = {"global": 0.0, "brazil": 0.0, "state": 0.0}
    breakdown = {}
    for sub, m_new in new_masses_by_substance.items():
        if sub not in cfs["cfs"]:
            continue
        cf = cfs["cfs"][sub]["cf_daly_per_kg"]
        breakdown[sub] = {
            "new_mass_total": m_new,
            "cf_global": cf["global"],
            "cf_brazil": cf["brazil"],
            "cf_state": cf["state"],
        }
        for k in new_gt:
            new_gt[k] += m_new * cf[k]

    return new_gt, breakdown, perturbed_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", type=int, default=1, choices=[1, 2, 3, 4])
    args = parser.parse_args()
    system = args.system

    lci, cfs, gt_data = load_system(system)
    original_gt = gt_data["ground_truth_economic"]

    out_dir = PROC / f"s{system}" / "stress"
    out_dir.mkdir(parents=True, exist_ok=True)

    schemes = ["P1", "P2", "P3"]
    for s in schemes:
        gt, breakdown, rows = gt_for_scheme(s, lci, cfs)
        write_markdown_table(rows, out_dir / f"lci_{s}.md")
        out = {
            "scheme": s,
            "system": system,
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
        with open(out_dir / f"gt_{s}.json", "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"S{system} {s}: new GT global = {gt['global']:.3e} "
              f"(×{gt['global']/original_gt['global']:.3f} vs original)")

    # Copy CF table (unchanged) so each prompt is self-contained
    cf_md_source = PROC / f"s{system}" / "cf_oberschelp.md"
    (out_dir / "cf_oberschelp.md").write_text(cf_md_source.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"\nFiles written to data/processed/s{system}/stress/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
