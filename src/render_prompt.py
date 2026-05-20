"""Render a prompt template by substituting placeholders.

Usage:
    python src/render_prompt.py --level L4 --lang pt-BR --system 1
    python src/render_prompt.py --level L4 --lang pt-BR --system 2 --output /tmp/L4_s2.md

Reads:
  - prompts/templates/_system_instruction_{lang_code}.md
  - prompts/templates/{lang}/{level}_*.md
  - data/processed/s{N}/emissions_air_pm.md     (for {{LCI_TABLE}})
  - data/processed/s{N}/cf_oberschelp.md        (for {{CF_TABLE_OBERSCHELP}})

State-name placeholders are filled per system:
  Sistema 1 -> São Paulo (SP)
  Sistema 2 -> Paraná (PR)
  Sistema 3 -> ? (auto-detected from ground_truth.json)
  Sistema 4 -> ? (auto-detected from ground_truth.json)
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "prompts" / "templates"
PROCESSED = ROOT / "data" / "processed"

LEVEL_FILES = {
    "L0": "L0_zero_context.md",
    "L1": "L1_scoped.md",
    "L2": "L2_with_lci.md",
    "L3": "L3_with_factors.md",
    "L4": "L4_with_procedure.md",
}

LANG_TO_SYSTEM_SUFFIX = {
    "pt-BR": "pt",
    "en": "en",
}


# State labels for each system (read dynamically from ground_truth.json if available)
def system_state_info(system: int) -> tuple[str, str, str]:
    """Return (state_code, state_name_pt, state_name_en) for the given system.

    state_name_pt already includes the correct preposition contraction
    (e.g. "Estado de São Paulo" vs "Estado do Paraná").
    """
    gt_path = PROCESSED / f"s{system}" / "ground_truth.json"
    if not gt_path.exists():
        raise FileNotFoundError(f"Run: python src/extract_system.py --system {system} first.")
    gt_data = json.loads(gt_path.read_text(encoding="utf-8"))
    code = gt_data.get("state_label") or "?"
    # PT-BR uses "Estado de [feminine/initial-vowel-stress]" or "Estado do [masculine]"
    state_pt_phrases = {
        "SP": "Estado de São Paulo",
        "PR": "Estado do Paraná",
        "MG": "Estado de Minas Gerais",
        "RS": "Estado do Rio Grande do Sul",
        "GO": "Estado de Goiás",
        "MT": "Estado de Mato Grosso",
        "MS": "Estado de Mato Grosso do Sul",
        "BA": "Estado da Bahia",
    }
    state_en_phrases = {
        "SP": "State of São Paulo",
        "PR": "State of Paraná",
        "MG": "State of Minas Gerais",
        "RS": "State of Rio Grande do Sul",
        "GO": "State of Goiás",
        "MT": "State of Mato Grosso",
        "MS": "State of Mato Grosso do Sul",
        "BA": "State of Bahia",
    }
    name_pt = state_pt_phrases.get(code, f"Estado de {code}")
    name_en = state_en_phrases.get(code, f"State of {code}")
    return code, name_pt, name_en


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render(level: str, lang: str, system: int = 1) -> str:
    if level not in LEVEL_FILES:
        raise ValueError(f"Unknown level: {level}. Use one of {list(LEVEL_FILES)}")
    if lang not in LANG_TO_SYSTEM_SUFFIX:
        raise ValueError(f"Unknown lang: {lang}. Use one of {list(LANG_TO_SYSTEM_SUFFIX)}")

    state_code, state_name_pt, state_name_en = system_state_info(system)

    sys_suffix = LANG_TO_SYSTEM_SUFFIX[lang]
    system_text = load(TEMPLATES / f"_system_instruction_{sys_suffix}.md")
    user = load(TEMPLATES / lang / LEVEL_FILES[level])

    if "{{LCI_TABLE}}" in user:
        lci = load(PROCESSED / f"s{system}" / "emissions_air_pm.md").strip()
        user = user.replace("{{LCI_TABLE}}", lci)
    if "{{CF_TABLE_OBERSCHELP}}" in user:
        cf = load(PROCESSED / f"s{system}" / "cf_oberschelp.md").strip()
        user = user.replace("{{CF_TABLE_OBERSCHELP}}", cf)

    for txt in (system_text, user):
        pass  # no-op, just for readability

    def apply_state_placeholders(s: str) -> str:
        return (s.replace("{{STATE_NAME_PT}}", state_name_pt)
                 .replace("{{STATE_NAME_EN}}", state_name_en)
                 .replace("{{STATE_CODE}}", state_code))

    system_text = apply_state_placeholders(system_text)
    user = apply_state_placeholders(user)

    return (
        "=" * 80 + f"\nSYSTEM INSTRUCTION (system {system}, state={state_code})\n" + "=" * 80 + "\n\n"
        + system_text.strip() + "\n\n"
        + "=" * 80 + f"\nUSER PROMPT — level={level} lang={lang} system=S{system}\n" + "=" * 80 + "\n\n"
        + user.strip() + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True, choices=list(LEVEL_FILES))
    parser.add_argument("--lang", default="pt-BR", choices=list(LANG_TO_SYSTEM_SUFFIX))
    parser.add_argument("--system", type=int, default=1, choices=[1, 2, 3, 4])
    parser.add_argument("--output", help="Optional output file; defaults to stdout")
    args = parser.parse_args()

    rendered = render(args.level, args.lang, args.system)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output} ({len(rendered)} chars)")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
