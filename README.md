# IA Aplicada ao Estudo de ACV

**Quão assertiva é a IA no cálculo de Avaliação do Ciclo de Vida?** Uma avaliação experimental por níveis progressivos de prompt, benchmarkada com a ACV regionalizada de impactos de material particulado em sistemas de produção leiteira no Brasil.

> *How assertive is AI in Life Cycle Assessment? An experimental evaluation through progressive prompt levels, benchmarked against a regionalized LCA of particulate matter impacts in Brazilian milk production systems.*

---

## Alvos de publicação

| Etapa | Alvo | Formato | Deadline |
|-------|------|---------|----------|
| **1** | [9º Congresso Brasileiro sobre Gestão do Ciclo de Vida (GCV 2026)](https://gcvbrasil.com) | Resumo expandido (5 pp, PDF) | A confirmar — chamada entre mai/ago 2026 |
| **2** | *International Journal of Life Cycle Assessment* (IJLCA) | Research article | Pós-evento |

**Local do evento**: Recife/PE, 17–19 de novembro de 2026. Tema: *"Ciclo de vida e digitalização para o desenvolvimento sustentável nos territórios"*.

---

## Paper-benchmark (ground truth)

Giusti, G., Vieira, J. G. V., **Tadano, Y. S.** (orientadora), Silva, D. A. L., Fantke, P. (2023). **Human health impacts of particulate matter emitted from different milk production systems in Brazil: a regionalized LCA sensitivity analysis.** *Int J Life Cycle Assess*. DOI: [10.1007/s11367-023-02184-8](https://doi.org/10.1007/s11367-023-02184-8)

A orientadora (Profa. Yara Tadano) é coautora do paper-benchmark — declarado em "conflict of interest". O tratamento metodológico será: comparar outputs da IA contra os números publicados, **sem reanálise privilegiada do dado bruto**.

---

## Escopo — Evento (reduzido) vs. Artigo IJLCA (expandido)

### Escopo evento (GCV 2026) — foco imediato

- **Sistema produtivo**: 1 (Inventário-S1)
- **Modelo de caracterização**: 1 (Oberschelp et al., 2020)
- **Alocação**: Econômica
- **Escopos geográficos**: Global, Brasil, Estado-SP (3 células de comparação)
- **Variável independente**: 5 níveis de prompt (L0–L4)
- **LLMs**: 4 modelos (Claude Opus 4.7, GPT, Gemini, Llama/DeepSeek)
- **Repetições**: n ≥ 5 por célula
- **Idiomas + jurisdições**: 3 idiomas × 3 VPS em países diferentes apenas em **L0** — para isolar viés de regionalização proveniente do *training data* (extensão metodológica)

**Total estimado (evento)**: 5 níveis × 4 LLMs × 3 escopos × 5 reps + (4 LLMs × 3 idiomas × 3 VPS × 5 reps no L0) ≈ 300 + 180 = ~480 outputs. Possível piloto de 100 outputs antes.

### Escopo artigo (IJLCA) — expansão posterior

- 4 sistemas produtivos × 5 modelos de caracterização × 3 níveis de regionalização = matriz 4×5×3 = **60 células** (mesmo grid do paper-benchmark)
- Ambas alocações (Mássica + Econômica)
- 2 idiomas (PT-BR / EN) + análise multi-jurisdição
- Total estimado: ~800–1500 outputs

Detalhes em [`SCOPE.md`](SCOPE.md).

---

## Estrutura do repositório

```
.
├── data/
│   ├── raw/                  # ACV-Sensibilidade.xlsx + Oberschelp 2020 SI
│   ├── processed/
│   └── ground_truth/         # Valores de referência extraídos
├── prompts/
│   ├── templates/            # L0..L4 (PT-BR + EN + ES futuramente)
│   └── runs/                 # Snapshot de prompts efetivamente executados
├── src/                      # Pipeline: chamadas API, métricas, análise
├── results/
│   ├── raw/                  # Outputs brutos das LLMs (JSON/JSONL)
│   ├── processed/            # CSVs/parquets agregados
│   └── figures/
├── manuscript/
│   ├── gcv2026/              # Resumo expandido (LaTeX)
│   └── ijlca/                # Artigo completo (posterior)
├── docs/                     # Proposta original, regras GCV 2026, Oberschelp 2020
├── notebooks/
└── tests/
```

---

## Setup rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

API keys necessárias (não commitadas): `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`. Ver `.env.example` (a criar).

---

## Reprodutibilidade

- Prompts versionados em `prompts/templates/` (read-only após snapshot).
- Cada chamada de API registra: timestamp, modelo, versão, temperatura, seed (quando suportado).
- Outputs brutos preservados em `results/raw/` (JSONL).
- Pré-registro no OSF antes da execução principal.
- Versão final dos dados + scripts: Zenodo (DOI) após submissão.

---

## Ética

- Sem seres humanos / animais.
- Uso de IA na própria elaboração do artigo declarado conforme **CNPq Portaria 2.664/2026** e prática Nature/Elsevier.
- Conflito de interesse declarado: orientadora é coautora do paper-benchmark.

---

## Equipe

- **Lucas Rover** ¹·² — ORCID: [0000-0001-6641-9224](https://orcid.org/0000-0001-6641-9224)
- **Profa. Dra. Yara de Souza Tadano** ¹ (orientadora)
- Demais coautores a definir.

¹ PPGSAU — UTFPR · ² Academia Lendária
