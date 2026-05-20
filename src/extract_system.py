"""Extract LCI and ground truth for any system (S1, S2, S3, S4).

Generalization of the original Sistema 1 extraction. Writes self-contained
artifacts per system in data/processed/{s1,s2,s3,s4}/.

Usage:
    python src/extract_system.py --system 2
"""

from __future__ import annotations
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "raw" / "ACV-Sensibilidade.xlsx"
OUT_BASE = ROOT / "data" / "processed"

# Tabela-AICV column layout (1-indexed)
# row 4 = Global, row 5 = Brazil, row 6 = State for Model 1 (Oberschelp)
AICV_ECON_COL = {1: 4, 2: 6, 3: 8, 4: 10}

# Caracterização sheet — find Sistema N economic columns
# row 1 = System number, row 2 = Allocation, row 3 = Model, row 4 = Geo scope
# Economic columns for each (Sistema N, Oberschelp): 3 cols (Global/Brasil/SP)
# Sistema 1 Econ Oberschelp -> cols 14, 15, 16
# Sistema 2 Econ Oberschelp -> shift by +(...) — need to detect dynamically
CARAC_OBERSCHELP_ECON_START_COL = {1: 14}  # Sistema 1 starts at col 14

# PM precursor substances (for filtering air emissions and CFs)
PM_SUBSTANCES = [
    "Ammonia",
    "Nitrogen oxides",
    "Sulfur dioxide",
    "Particulates, < 2.5 um",
    "Particulates, > 2.5 um, and < 10um",
    "Particulates, > 10 um",
    "Sulfur trioxide",
    "Sulfur monoxide",
]

# Inventory sheet name pattern
SYSTEM_INVENTORY_SHEET = "Inventário-S{n}-Completo"

# Sheet layout (same for all systems)
INV_ECON_OUTPUTS_COLS = {  # 1-indexed
    "uuid": 23,
    "flow": 24,
    "category": 25,
    "subcategory": 26,
    "unit": 27,
    "value": 28,
}


def strip_country_suffix(flow: str) -> str:
    return re.sub(r",\s*[A-Z]{2,3}(\s+\([^)]*\))?$", "", str(flow)).strip()


def simplify_subcat(s: str) -> str:
    s = str(s).lower()
    if "high population" in s:
        return "high population density"
    if "low population density, long-term" in s:
        return "low population density (long-term)"
    if "low population" in s:
        return "low population density"
    if "unspecified" in s:
        return "unspecified"
    if "stratosphere" in s:
        return "lower stratosphere + upper troposphere"
    if "industrial" in s:
        return "industrial"
    if "forestry" in s:
        return "forestry"
    return s


def find_carac_oberschelp_econ_cols(wb, system: int) -> tuple[dict, str]:
    """Locate (Global, Brasil, State) cols for (Sistema N × Oberschelp × Econômica).

    Returns (cols_dict, state_label).  State label varies per system
    (S1 = SP, S2 = PR, etc.).
    """
    ws = wb["Caracterização"]
    target = {"global": None, "brazil": None, "state": None}
    state_label = None
    for col in range(1, ws.max_column + 1):
        s_num = ws.cell(row=1, column=col).value
        alloc = ws.cell(row=2, column=col).value
        model = ws.cell(row=3, column=col).value
        geo = ws.cell(row=4, column=col).value
        if (str(s_num) == str(system)
                and str(alloc).strip().lower() in {"economica", "econômica"}
                and "Oberschelp" in str(model)):
            if geo == "Global":
                target["global"] = col
            elif geo == "Brasil":
                target["brazil"] = col
            elif geo and "Estado" in str(geo):
                target["state"] = col
                state_label = str(geo).replace("Estado - ", "").strip()
    if None in target.values():
        raise RuntimeError(f"Could not locate Caracterização cols for system {system}: {target}")
    return target, state_label


def extract_lci(wb, system: int) -> dict:
    """Aggregate PM-relevant air emissions for system N (economic allocation)."""
    sheet_name = SYSTEM_INVENTORY_SHEET.format(n=system)
    ws = wb[sheet_name]
    c = INV_ECON_OUTPUTS_COLS

    raw_air = []
    for r in range(6, ws.max_row + 1):
        flow = ws.cell(row=r, column=c["flow"]).value
        subcat = ws.cell(row=r, column=c["subcategory"]).value
        unit = ws.cell(row=r, column=c["unit"]).value
        value = ws.cell(row=r, column=c["value"]).value
        if flow is None or value is None:
            continue
        if subcat and any(k in str(subcat) for k in [
            "population density", "unspecified", "stratosphere",
            "long-term", "industrial", "forestry"
        ]):
            raw_air.append({"flow": str(flow), "subcat": str(subcat),
                            "unit": unit, "value": float(value)})

    agg = defaultdict(lambda: {"value": 0.0, "unit": None, "n_flows": 0})
    for e in raw_air:
        fam = strip_country_suffix(e["flow"])
        sub = simplify_subcat(e["subcat"])
        key = (fam, sub, e["unit"])
        agg[key]["value"] += e["value"]
        agg[key]["unit"] = e["unit"]
        agg[key]["n_flows"] += 1

    records = []
    for (fam, sub, unit), v in agg.items():
        if abs(v["value"]) > 1e-20:
            records.append({
                "substance": fam, "compartment": sub, "unit": unit,
                "value": v["value"], "aggregated_from_n_flows": v["n_flows"]
            })

    pm_records = [r for r in records if r["substance"] in PM_SUBSTANCES]

    def sort_key(rec):
        return (-abs(rec["value"]),)
    pm_records.sort(key=sort_key)
    return {"raw_count": len(raw_air), "pm_relevant_flows": pm_records}


def extract_gt(wb, system: int) -> dict:
    """Get published ground truth (Sistema N, Oberschelp Average, Econômica).

    Key 'state' refers to the system-specific state (S1=SP, S2=PR, S3=?, S4=?).
    """
    ws = wb["Tabela-AICV"]
    col = AICV_ECON_COL[system]
    return {
        "global":   ws.cell(row=4, column=col).value,
        "brazil":   ws.cell(row=5, column=col).value,
        "state":    ws.cell(row=6, column=col).value,
    }


def compute_effective_cfs(wb, system: int, lci_pm_records: list[dict], gt: dict) -> dict:
    """Compute effective CFs and cross-check against published GT.

    Note: the published GT in column 'state' refers to the system-specific
    state (S1=SP, S2=PR, ...), kept under the key 'state' in both the GT
    and CF outputs.
    """
    ws = wb["Caracterização"]
    cols, state_label = find_carac_oberschelp_econ_cols(wb, system)

    # Targets: PM precursors. Note: each substance may appear in MULTIPLE
    # TOTAL rows (e.g. "Ammonia" national + "Ammonia - internacional" for
    # upstream foreign emissions). We sum all of them per substance.
    targets = ["Ammonia", "Nitrogen oxides", "Sulfur dioxide", "Particulates, < 2.5 um"]
    total_rows = defaultdict(list)
    for r in range(7, ws.max_row + 1):
        sub = ws.cell(row=r, column=1).value
        comp = ws.cell(row=r, column=2).value
        if sub and comp and "TOTAL" in str(comp):
            # Strip country suffix AND "- internacional" / "- international" markers
            sub_main = strip_country_suffix(str(sub))
            sub_main = re.sub(r"\s*-\s*internacional$", "", sub_main, flags=re.IGNORECASE).strip()
            sub_main = re.sub(r"\s*-\s*international$", "", sub_main, flags=re.IGNORECASE).strip()
            if sub_main in targets:
                total_rows[sub_main].append(r)

    mass_by_sub = defaultdict(float)
    for r in lci_pm_records:
        mass_by_sub[r["substance"]] += r["value"]

    cfs = {}
    sums = {"global": 0.0, "brazil": 0.0, "state": 0.0}
    for sub, rows in total_rows.items():
        daly = {"global": 0.0, "brazil": 0.0, "state": 0.0}
        for row in rows:
            for scope_key, col_idx in [("global", cols["global"]),
                                        ("brazil", cols["brazil"]),
                                        ("state",  cols["state"])]:
                val = ws.cell(row=row, column=col_idx).value
                if isinstance(val, (int, float)):
                    daly[scope_key] += val
        m = mass_by_sub.get(sub, 0)
        if m == 0:
            continue
        cfs[sub] = {
            "mass_kg_per_kg_fpcm": m,
            "cf_daly_per_kg": {k: (daly[k] / m if m else None) for k in daly},
            "aggregated_from_total_rows": rows,
        }
        for k in sums:
            sums[k] += daly[k]

    check = {k: {"computed_sum": sums[k], "published_gt": gt[k],
                 "rel_diff_pct": (sums[k] - gt[k]) / gt[k] * 100 if gt[k] else None}
             for k in sums}
    return {"cfs": cfs, "check": check, "state_label": state_label}


def write_outputs(system: int, lci: dict, gt: dict, cf_data: dict) -> None:
    out_dir = OUT_BASE / f"s{system}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # LCI files
    lci_full = {
        "source": f"Inventário-S{system}-Completo, Alocação Econômica",
        "system": f"Sistema {system}",
        "functional_unit": "1 kg FPCM",
        "allocation": "economic",
        "pm_relevant_flows": lci["pm_relevant_flows"],
        "total_raw_flows_aggregated": lci["raw_count"],
    }
    (out_dir / "emissions_air.json").write_text(
        json.dumps(lci_full, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = "| Substância | Compartimento | Quantidade (kg / kg FPCM) |\n|---|---|---|\n"
    for r in lci["pm_relevant_flows"]:
        md += f"| {r['substance']} | {r['compartment']} | {r['value']:.4e} |\n"
    (out_dir / "emissions_air_pm.md").write_text(md, encoding="utf-8")

    # Ground truth
    gt_full = {
        "paper": "Giusti et al. (2023)",
        "doi": "10.1007/s11367-023-02184-8",
        "scope": f"Sistema {system} × Oberschelp et al. (2020) × Alocação Econômica",
        "unit": "DALY/kg FPCM",
        "state_label": cf_data.get("state_label"),
        "ground_truth_economic": gt,
    }
    (out_dir / "ground_truth.json").write_text(
        json.dumps(gt_full, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # CFs (effective, validated against native Oberschelp SI)
    cf_full = {
        "model": "Oberschelp et al. (2020)",
        "effect_model": "Average",
        "allocation": "economic",
        "system": f"Sistema {system}",
        "cfs": cf_data["cfs"],
        "ground_truth_reconstruction_check": cf_data["check"],
    }
    (out_dir / "cf_oberschelp.json").write_text(
        json.dumps(cf_full, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    state_label = cf_data.get("state_label") or "?"
    cf_md = f"""**Modelo de caracterização**: Oberschelp et al. (2020). DOI: 10.1021/acs.est.0c05691
**Modelo de efeito**: `Average` · **Altura**: `Ground level` · **Tempo**: anual, dia-noite

| Substância | Massa total emitida (kg / kg FPCM) | CF Global (DALY/kg) | CF Brasil (DALY/kg) | CF Estado-{state_label} (DALY/kg) |
|---|---|---|---|---|
"""
    short = {"Ammonia": "NH3", "Nitrogen oxides": "NOx",
             "Particulates, < 2.5 um": "PM2.5", "Sulfur dioxide": "SO2"}
    for sub, d in cf_data["cfs"].items():
        cf_md += f"| {sub} ({short.get(sub, sub)}) | {d['mass_kg_per_kg_fpcm']:.3e} | {d['cf_daly_per_kg']['global']:.3e} | {d['cf_daly_per_kg']['brazil']:.3e} | {d['cf_daly_per_kg']['state']:.3e} |\n"
    (out_dir / "cf_oberschelp.md").write_text(cf_md, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()
    sys_n = args.system

    print(f"Loading workbook...")
    wb = openpyxl.load_workbook(XLSX, data_only=True)

    print(f"Extracting LCI for Sistema {sys_n}...")
    lci = extract_lci(wb, sys_n)
    print(f"  PM-relevant flows: {len(lci['pm_relevant_flows'])} (from {lci['raw_count']} raw)")

    print(f"Extracting ground truth...")
    gt = extract_gt(wb, sys_n)
    print(f"  Global : {gt['global']:.4e}")
    print(f"  Brazil : {gt['brazil']:.4e}")
    print(f"  State  : {gt['state']:.4e}")

    print(f"Computing effective CFs and cross-checking...")
    cf_data = compute_effective_cfs(wb, sys_n, lci["pm_relevant_flows"], gt)
    for scope, c in cf_data["check"].items():
        print(f"  {scope:10s}: sum={c['computed_sum']:.4e}  GT={c['published_gt']:.4e}  diff={c['rel_diff_pct']:+.3f}%")

    write_outputs(sys_n, lci, gt, cf_data)
    print(f"\nWrote outputs to data/processed/s{sys_n}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
