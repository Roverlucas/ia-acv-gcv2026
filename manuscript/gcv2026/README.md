# Resumo expandido — GCV 2026

Pasta self-contained pronta para uso no Overleaf. Compila standalone (sem depender de paths externos ao diretório `manuscript/gcv2026/`).

## Como usar no Overleaf

### Opção 1 — Overleaf Premium (GitHub sync)
1. New Project → Import from GitHub → selecionar `Roverlucas/ia-acv-gcv2026`
2. Configurar `Main document` para `manuscript/gcv2026/resumo-expandido.tex`
3. Pull/Push direto pela interface Overleaf

### Opção 2 — Upload manual (Overleaf gratuito)
1. Comprimir a pasta `manuscript/gcv2026/` em um zip
2. New Project → Upload Project → escolher o zip
3. Compile (LaTeX Engine: `pdfLaTeX` ou `XeLaTeX`)

```bash
cd manuscript/gcv2026
zip -r resumo-overleaf.zip resumo-expandido.tex figures tables README.md
```

## Compilação local

```bash
cd manuscript/gcv2026
tectonic resumo-expandido.tex          # recomendado (self-contained)
# OU
pdflatex resumo-expandido.tex
```

## Estrutura

```
manuscript/gcv2026/
├── resumo-expandido.tex   ← main (5 páginas, anônimo, Times 12pt, A4)
├── resumo-expandido.pdf   ← saída compilada
├── figures/               ← PDFs auto-contidos (gerados por src/figures.py)
│   ├── fig1_mape_vs_level.pdf
│   └── fig4_agreement_share.pdf
├── tables/                ← fragmentos LaTeX (gerados por src/generate_tables.py)
│   ├── tbl_summary.tex
│   ├── tbl_charmodel.tex
│   └── tbl_agreement.tex
└── README.md
```

## Regras GCV 2026 (já aplicadas)

- ✅ Formato PDF
- ✅ Máx. 5 páginas
- ✅ A4, margens 3-2-3-2 cm
- ✅ Times New Roman 12pt (via `mathptmx`)
- ✅ Alinhamento justificado, espaçamento simples
- ✅ Numeração de página inferior-direita
- ✅ Estrutura: Introdução, Metodologia, Resultados, Conclusões
- ✅ Anônimo (autoria omitida)
- ✅ Referências NBR-6023 ABNT

## Checklist pré-submissão

- [ ] **Verificar se a chamada está aberta** em https://gcvbrasil.com
- [ ] **Limpar metadata do PDF** (autoria nas propriedades):
      `exiftool -all= resumo-expandido.pdf`
- [ ] **Revisão da Yara** (coautora do paper-benchmark — conflito de interesse declarado)
- [ ] **Pré-registro OSF** (recomendado para credibilidade)
- [ ] Confirmar coautoria com Giusti, Silva, Vieira, Fantke?

## Regenerar figuras/tabelas

A partir do diretório raiz do repo:

```bash
source .venv/bin/activate
python src/analyze.py --exclude-smoke   # processa results/raw/*.jsonl
python src/figures.py                    # gera PDFs em results/figures/
python src/generate_tables.py            # gera .tex em manuscript/gcv2026/tables/

# Atualizar figuras self-contained na pasta do manuscrito:
cp results/figures/fig1_mape_vs_level.pdf manuscript/gcv2026/figures/
cp results/figures/fig4_agreement_share.pdf manuscript/gcv2026/figures/
```
