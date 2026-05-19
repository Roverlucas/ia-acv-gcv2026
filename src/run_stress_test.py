"""Run the H6 contamination stress test.

For each perturbation scheme P1/P2/P3, runs L3 and L4 with the perturbed
inventory injected, keeping CFs (Oberschelp) and the system prompt unchanged.

Each call's record carries:
  - the new ground truth I'_g (computed deterministically before the run)
  - both "err_vs_new_gt" and "err_vs_original_gt" so we can tell
    calculation from memorization.

Usage:
    python src/run_stress_test.py                       # full run
    python src/run_stress_test.py --providers gpt       # one LLM
    python src/run_stress_test.py --dry-run             # preview only
"""

from __future__ import annotations
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from llm_clients import call_llm  # noqa: E402
from run_experiment import hash_prompt, parse_json_response, parse_json_lenient  # noqa: E402

TEMPLATES = ROOT / "prompts" / "templates"
STRESS = ROOT / "data" / "processed" / "stress"
RESULTS_DIR = ROOT / "results" / "raw"
CONFIG_PATH = ROOT / "src" / "llm_config.yaml"

LEVEL_FILES = {"L3": "L3_with_factors.md", "L4": "L4_with_procedure.md"}
SCHEMES = ["P1", "P2", "P3"]
LANG = "pt-BR"  # stress test in PT-BR only (cheaper, sufficient for H6)
REPS = 5


def load_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def render(level: str, scheme: str) -> tuple[str, str]:
    system = (TEMPLATES / "_system_instruction_pt.md").read_text(encoding="utf-8").strip()
    user = (TEMPLATES / LANG / LEVEL_FILES[level]).read_text(encoding="utf-8")
    lci = (STRESS / f"lci_{scheme}.md").read_text(encoding="utf-8").strip()
    cf = (STRESS / "cf_oberschelp_s1.md").read_text(encoding="utf-8").strip()
    user = user.replace("{{LCI_TABLE}}", lci).replace("{{CF_TABLE_OBERSCHELP}}", cf)
    # Add a header to the prompt noting that the inventory is hypothetical
    note = (
        "\n\n> **Nota experimental**: o inventário abaixo é hipotético "
        "(perturbação controlada do inventário original do Sistema 1) e "
        "destinado a um teste de robustez. Faça o cálculo com base estritamente "
        "nos números fornecidos.\n"
    )
    # Inject the note right after the first '---' separator
    user = user.replace("---", "---" + note, 1)
    return system, user


def load_new_gt(scheme: str) -> dict:
    return json.loads((STRESS / f"gt_{scheme}.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--providers", default="gpt,gemini,deepseek")
    parser.add_argument("--schemes", default="P1,P2,P3")
    parser.add_argument("--levels", default="L3,L4")
    parser.add_argument("--reps", type=int, default=REPS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    cfg = load_config()
    models = {m["id"]: m for m in cfg["models"]}

    providers = args.providers.split(",")
    schemes = args.schemes.split(",")
    levels = args.levels.split(",")
    reps = args.reps

    runs = []
    for prov in providers:
        for scheme in schemes:
            new_gt_data = load_new_gt(scheme)
            for level in levels:
                for rep in range(1, reps + 1):
                    runs.append({
                        "provider": prov,
                        "model_id": models[prov]["api_model_id"],
                        "level": level,
                        "scheme": scheme,
                        "language": LANG,
                        "rep": rep,
                        "temperature": 0.0,
                        "new_ground_truth": new_gt_data["new_ground_truth"],
                        "original_ground_truth": new_gt_data["original_ground_truth"],
                        "ratio_new_over_original": new_gt_data["ratio_new_over_original"],
                        "scheme_description": new_gt_data["description"],
                    })

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Stress test: {len(runs)} runs.")
    print(f"  Providers: {providers} · Schemes: {schemes} · Levels: {levels} · Reps: {reps}")
    if args.dry_run:
        for r in runs:
            print(f"  {r['provider']:10s} {r['level']} {r['scheme']} rep={r['rep']} "
                  f"new_gt_global={r['new_ground_truth']['global']:.3e}")
        return 0

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "__stress"
    out_path = RESULTS_DIR / f"{run_id}.jsonl"

    n_ok = n_err = n_parse_fail = 0
    t_start = time.time()
    with open(out_path, "w", encoding="utf-8") as f:
        for i, run in enumerate(runs, 1):
            system, user = render(run["level"], run["scheme"])
            prompt_hash = hash_prompt(system + "\n\n" + user)

            max_tokens = 16384 if run["provider"] == "gemini" else 4096
            t0 = time.time()
            resp = call_llm(
                provider=run["provider"],
                model_id=run["model_id"],
                system=system,
                user=user,
                temperature=run["temperature"],
                max_tokens=max_tokens,
                seed=42,
            )
            elapsed = time.time() - t0
            resp_dict = resp.to_dict()
            text = resp_dict.get("text") or ""
            parsed, parse_err = parse_json_response(text)
            parsed_lenient, _ = (None, None)
            if parsed is None:
                parsed_lenient, _ = parse_json_lenient(text)

            record = {
                **run,
                "prompt_hash": prompt_hash,
                "response": resp_dict,
                "parsed_output": parsed,
                "parsed_output_lenient": parsed_lenient,
                "parse_error": parse_err,
                "lenient_recovered": parsed_lenient is not None and parsed is None,
            }
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
            f.flush()

            err = resp_dict.get("error")
            if err:
                n_err += 1
                status = f"ERR ({err[:50]})"
            elif parse_err and parsed_lenient is None:
                n_parse_fail += 1
                status = "PARSE_FAIL"
            else:
                n_ok += 1
                p = parsed or parsed_lenient or {}
                ans_g = (p.get("answer") or {}).get("global", {}).get("value")
                if isinstance(ans_g, (int, float)):
                    err_new = (ans_g - run["new_ground_truth"]["global"]) / run["new_ground_truth"]["global"] * 100
                    err_orig = (ans_g - run["original_ground_truth"]["global"]) / run["original_ground_truth"]["global"] * 100
                    status = f"OK ans={ans_g:.2e} ΔnewGT={err_new:+.0f}% ΔorigGT={err_orig:+.0f}%"
                else:
                    status = "OK (null)"

            print(f"  [{i:2d}/{len(runs)}] {run['provider']:10s} {run['scheme']} {run['level']} "
                  f"rep={run['rep']} t={elapsed:5.1f}s  {status}")

    total = time.time() - t_start
    print(f"\nDone. {out_path.name}")
    print(f"  OK: {n_ok} · ERR: {n_err} · PARSE_FAIL: {n_parse_fail}")
    print(f"  Total elapsed: {total/60:.1f} min")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
