"""Render a prompt template by substituting placeholders.

Usage:
    python src/render_prompt.py --level L4 --lang pt-BR --output /tmp/L4_rendered.md

Reads:
  - prompts/templates/_system_instruction_{lang_code}.md
  - prompts/templates/{lang}/{level}_*.md
  - data/processed/sistema1_emissions_air_pm.md     (for {{LCI_TABLE}})
  - data/processed/cf_oberschelp_s1.md              (for {{CF_TABLE_OBERSCHELP}})

Writes the fully rendered prompt to stdout or --output.
"""

from __future__ import annotations
import argparse
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


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render(level: str, lang: str) -> str:
    if level not in LEVEL_FILES:
        raise ValueError(f"Unknown level: {level}. Use one of {list(LEVEL_FILES)}")
    if lang not in LANG_TO_SYSTEM_SUFFIX:
        raise ValueError(f"Unknown lang: {lang}. Use one of {list(LANG_TO_SYSTEM_SUFFIX)}")

    sys_suffix = LANG_TO_SYSTEM_SUFFIX[lang]
    system = load(TEMPLATES / f"_system_instruction_{sys_suffix}.md")
    user = load(TEMPLATES / lang / LEVEL_FILES[level])

    if "{{LCI_TABLE}}" in user:
        lci = load(PROCESSED / "sistema1_emissions_air_pm.md").strip()
        user = user.replace("{{LCI_TABLE}}", lci)
    if "{{CF_TABLE_OBERSCHELP}}" in user:
        cf = load(PROCESSED / "cf_oberschelp_s1.md").strip()
        user = user.replace("{{CF_TABLE_OBERSCHELP}}", cf)

    return (
        "=" * 80 + "\nSYSTEM INSTRUCTION\n" + "=" * 80 + "\n\n"
        + system.strip() + "\n\n"
        + "=" * 80 + f"\nUSER PROMPT — level={level} lang={lang}\n" + "=" * 80 + "\n\n"
        + user.strip() + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True, choices=list(LEVEL_FILES))
    parser.add_argument("--lang", default="pt-BR", choices=list(LANG_TO_SYSTEM_SUFFIX))
    parser.add_argument("--output", help="Optional output file; defaults to stdout")
    args = parser.parse_args()

    rendered = render(args.level, args.lang)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output} ({len(rendered)} chars)")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
