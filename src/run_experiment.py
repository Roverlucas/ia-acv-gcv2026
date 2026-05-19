"""Orquestrador de experimento — IA Aplicada ao Estudo de ACV.

Uso:
    # smoke test: 1 chamada por (provider × nível × idioma)
    python src/run_experiment.py --smoke-test

    # piloto F1: 1 modelo × todos níveis × PT-BR × 3 escopos × 5 reps
    python src/run_experiment.py --provider gpt --langs pt-BR --reps 5

    # F2 completo
    python src/run_experiment.py --reps 5 --langs pt-BR,en

Salva resultados em results/raw/<timestamp>__<run_id>.jsonl (1 linha por chamada).
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Repo paths
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from llm_clients import call_llm  # noqa: E402
from render_prompt import render  # noqa: E402

CONFIG_PATH = ROOT / "src" / "llm_config.yaml"
RESULTS_DIR = ROOT / "results" / "raw"
PROMPT_RUNS_DIR = ROOT / "prompts" / "runs"

LEVELS = ["L0", "L1", "L2", "L3", "L4"]
DEFAULT_LANGS = ["pt-BR"]
DEFAULT_TEMP = 0.0


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def hash_prompt(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def parse_json_response(text: str) -> tuple[dict | None, str | None]:
    """Try to parse the JSON response. Tolerate markdown fences."""
    if not text:
        return None, "empty response"
    s = text.strip()
    # Strip markdown fences if present
    if s.startswith("```"):
        lines = s.splitlines()
        # Drop first line (```json or ```) and last line if ```
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    try:
        return json.loads(s), None
    except json.JSONDecodeError as e:
        return None, f"JSONDecodeError: {e}"


def build_runs(
    cfg: dict,
    providers: list[str],
    levels: list[str],
    langs: list[str],
    reps: int,
    temperature: float,
) -> list[dict]:
    """Generate the flat list of runs to execute."""
    models = {m["id"]: m for m in cfg["models"] if m["id"] in providers}
    runs = []
    for provider, level, lang, rep in product(providers, levels, langs, range(1, reps + 1)):
        model = models[provider]
        runs.append({
            "provider": provider,
            "model_id": model["api_model_id"],
            "level": level,
            "language": lang,
            "rep": rep,
            "temperature": temperature,
        })
    return runs


def run_one(run: dict, save_prompt: bool = True) -> dict:
    """Execute one call and return the merged result dict."""
    # Render prompt
    rendered = render(level=run["level"], lang=run["language"])
    # Extract system and user pieces from the rendered text
    parts = rendered.split("=" * 80)
    # render() output is:
    #   ====...\nSYSTEM INSTRUCTION\n====...\n<system>\n====...\nUSER PROMPT...\n====...\n<user>
    # We rebuild by reading the source files directly:
    from render_prompt import LEVEL_FILES, LANG_TO_SYSTEM_SUFFIX, TEMPLATES, PROCESSED
    sys_suffix = LANG_TO_SYSTEM_SUFFIX[run["language"]]
    system = (TEMPLATES / f"_system_instruction_{sys_suffix}.md").read_text(encoding="utf-8").strip()
    user = (TEMPLATES / run["language"] / LEVEL_FILES[run["level"]]).read_text(encoding="utf-8")
    if "{{LCI_TABLE}}" in user:
        user = user.replace("{{LCI_TABLE}}", (PROCESSED / "sistema1_emissions_air_pm.md").read_text(encoding="utf-8").strip())
    if "{{CF_TABLE_OBERSCHELP}}" in user:
        user = user.replace("{{CF_TABLE_OBERSCHELP}}", (PROCESSED / "cf_oberschelp_s1.md").read_text(encoding="utf-8").strip())

    prompt_hash = hash_prompt(system + "\n\n" + user)

    if save_prompt:
        PROMPT_RUNS_DIR.mkdir(parents=True, exist_ok=True)
        runfile = PROMPT_RUNS_DIR / f"{run['language']}_{run['level']}_{prompt_hash}.md"
        if not runfile.exists():
            runfile.write_text(
                f"## SYSTEM\n\n{system}\n\n## USER\n\n{user}\n",
                encoding="utf-8",
            )

    # API call — Gemini 2.5 needs more room because of internal "thinking" tokens
    max_tokens = 16384 if run["provider"] == "gemini" else 4096
    resp = call_llm(
        provider=run["provider"],
        model_id=run["model_id"],
        system=system,
        user=user,
        temperature=run["temperature"],
        max_tokens=max_tokens,
        seed=42,
    )
    resp_dict = resp.to_dict()

    # Parse JSON output (strict + lenient fallback)
    text = resp_dict.get("text") or ""
    parsed, parse_err = parse_json_response(text)
    parsed_lenient, lenient_err = (None, None)
    if parsed is None:
        parsed_lenient, lenient_err = parse_json_lenient(text)

    return {
        **run,
        "prompt_hash": prompt_hash,
        "response": resp_dict,
        "parsed_output": parsed,
        "parse_error": parse_err,
        "parsed_output_lenient": parsed_lenient,
        "lenient_recovered": parsed_lenient is not None and parsed is None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true",
                        help="1 chamada por (provider × nível × idioma); --reps e --temperature ignorados")
    parser.add_argument("--providers", default="gpt,gemini,deepseek",
                        help="Comma-separated provider ids (gpt,gemini,deepseek)")
    parser.add_argument("--levels", default="L0,L1,L2,L3,L4")
    parser.add_argument("--langs", default="pt-BR")
    parser.add_argument("--reps", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMP)
    parser.add_argument("--dry-run", action="store_true", help="Apenas listar runs sem executar")
    parser.add_argument("--max-runs", type=int, default=None)
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    cfg = load_config()

    providers = args.providers.split(",")
    levels = args.levels.split(",")
    langs = args.langs.split(",")

    if args.smoke_test:
        reps = 1
        temperature = 0.0
    else:
        reps = args.reps
        temperature = args.temperature

    runs = build_runs(cfg, providers, levels, langs, reps, temperature)
    if args.max_runs:
        runs = runs[: args.max_runs]

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Planning {len(runs)} runs.")
    print(f"  Providers: {providers} · Levels: {levels} · Langs: {langs} · Reps: {reps} · T: {temperature}")

    if args.dry_run:
        for r in runs:
            print(f"  {r['provider']:10s} {r['model_id']:30s} {r['level']:3s} {r['language']:6s} rep={r['rep']}")
        return 0

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}__{'smoke' if args.smoke_test else 'main'}"
    out_path = RESULTS_DIR / f"{run_id}.jsonl"

    n_ok = n_err = n_parse_fail = 0
    t_start = time.time()
    with open(out_path, "w", encoding="utf-8") as f:
        for i, run in enumerate(runs, 1):
            t0 = time.time()
            try:
                result = run_one(run)
            except Exception as e:
                result = {**run, "fatal_error": f"{type(e).__name__}: {e}"}
            elapsed = time.time() - t0

            # Status
            err = (result.get("response") or {}).get("error")
            parse_err = result.get("parse_error")
            if err:
                n_err += 1
                status = f"ERR  ({err[:60]})"
            elif parse_err:
                n_parse_fail += 1
                status = f"PARSE_FAIL ({parse_err[:60]})"
            else:
                n_ok += 1
                status = "OK"

            f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")
            f.flush()
            print(f"  [{i:3d}/{len(runs)}] {run['provider']:10s} {run['level']:3s} {run['language']:6s} "
                  f"t={elapsed:5.1f}s {status}")

    total_t = time.time() - t_start
    print(f"\nDone. Wrote {out_path}")
    print(f"  OK: {n_ok} · ERR: {n_err} · PARSE_FAIL: {n_parse_fail}")
    print(f"  Total elapsed: {total_t:.1f}s ({total_t / max(len(runs),1):.1f}s avg)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
