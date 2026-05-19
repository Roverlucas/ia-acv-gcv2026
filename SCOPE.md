# SCOPE — Escopo experimental versionado

> Documento vivo. Mudanças de escopo entram aqui antes de qualquer execução.
> Versão atual: **v0.2** (2026-05-19) — *Claude removido por orçamento; ES adiado para IJLCA*.

---

## 1. Fases

| Fase | Alvo | Escopo | Status |
|------|------|--------|--------|
| **F0** | Setup + ground truth | Estrutura repo + extração GT | ✅ |
| **F1** | Piloto | 1 sistema × 1 modelo × 3 escopos × 3 LLMs × 5 níveis × 5 reps PT-BR (~225) | 🔲 |
| **F2** | Evento GCV 2026 | F1 + extensão L0 multi-idioma (PT+EN) / multi-VPS (~210) | 🔲 |
| **F3** | Artigo IJLCA | 4 sistemas × 5 modelos × 3 escopos × ambas alocações × 2 idiomas (+ ES no L0) | 🔲 |

---

## 2. Escopo F1/F2 (Evento GCV 2026) — REDUZIDO

### 2.1 Ground truth (paper-benchmark Giusti et al. 2023)

Sistema 1 × Oberschelp et al. (2020) × Alocação Econômica → **3 células**:

| Escopo geográfico | Valor (DALY / kg FPCM) |
|-------------------|------------------------|
| Global            | 2.8297 × 10⁻⁸          |
| Brasil            | 8.1077 × 10⁻⁸          |
| Estado de SP      | 6.3727 × 10⁻⁷          |

**Range Global ↔ Estado-SP**: ~22.5×. Esse é o *sinal* que a IA precisa recuperar quando regionaliza.

Fonte: `data/ground_truth/sistema1_oberschelp_economica.json`.

### 2.2 Variável independente — níveis de prompt (L0–L4)

| Nível | Conteúdo entregue à IA | Pergunta-alvo |
|-------|------------------------|---------------|
| **L0** | Apenas pergunta geral | *"Em um estudo de ACV de produção de leite no Brasil, qual é o impacto do material particulado na saúde humana, em DALY/kg FPCM?"* |
| **L1** | L0 + escopo definido (UF, fronteira do sistema, categoria de impacto, região) | + especificações ISO-style |
| **L2** | L1 + inventário (LCI) bruto do Sistema 1 | "Calcule a partir destes dados" |
| **L3** | L2 + lista de fatores de caracterização disponíveis (Oberschelp 2020) | "Calcule usando estes fatores" |
| **L4** | L3 + descrição explícita do processo de cálculo, regras de regionalização e fórmulas | "Aplique este procedimento aos dados" |

**Justificativa para 5 níveis** (não 4): separar "zero context" (L0) de "scoped question" (L1) isola o efeito de simplesmente *delimitar o problema* do efeito de *fornecer dados*.

### 2.3 Modelos LLM (3 modelos — decisão de orçamento)

| # | Modelo | Vendor | Origem | Justificativa |
|---|--------|--------|--------|---------------|
| 1 | **GPT** (4.1 ou 5, frontier no momento da execução) | OpenAI | EUA | Maior adesão pública em ACV / praticantes; cutoff posterior a 2023 (testa H6) |
| 2 | **Gemini** (2.5 Pro ou frontier) | Google | EUA | Multilíngue forte; integração Workspace acadêmico |
| 3 | **DeepSeek V3** (ou frontier open equivalente) | DeepSeek | China | Open-source + viés geopolítico de treinamento distinto — **necessário para H7** |

**Excluído por custo**: Claude Opus 4.7 (Anthropic). Decisão registrada em 2026-05-19.

**Parâmetros de chamada**:
- Temperatura: fixa em 0.0 e 0.7 em runs separados
- Seed: quando suportado pelo provedor
- Versão exata da API: registrada em metadata de cada chamada (`results/raw/<run_id>.jsonl`)
- Cutoff de cada modelo: registrado para análise de H6

### 2.4 Extensão L0 multilíngue + multi-jurisdição

Apenas no nível **L0** (mais sensível a viés de treinamento), replicar em:

- **2 idiomas**: PT-BR, EN (escopo reduzido — ES adiado para fase IJLCA)
- **3 VPS** em países diferentes: BR, EU, US (a definir hosts específicos)

Hipótese (H7): a IA pode retornar fatores diferentes em função do *país aparente* da requisição e do idioma do prompt — replicando o viés de "amostra dominante" no corpus de treinamento. Com 3 modelos de origens diferentes (US × US × China), o contraste geopolítico é detectável.

### 2.5 Variáveis dependentes

**A — Acurácia numérica** (1-a-1 vs. GT):

- Erro relativo absoluto por célula
- MAPE (Mean Absolute Percentage Error)
- RMSE log-transformado
- Bland–Altman para concordância

**B — Corretude metodológica** (rubrica 0–3 com dupla rotulagem cega; Cohen κ ≥ 0.80):

- Modelo de caracterização declarado (correto / aceitável / inadequado)
- Nível de regionalização declarado (global / nacional / regional)
- Unidades dimensionalmente consistentes (sim/não)
- Aplicação de fatores de alocação (sim/não)

**C — Fidelidade regional**:

- A resposta diferencia regiões brasileiras? (binário)
- Direção coincide com Giusti et al.? (sim/não/parcial)
- Magnitude da diferenciação regional vs. paper (razão)

**D — Confiabilidade e alucinação**:

- Taxa de alucinação numérica (valores citados sem fonte verificável)
- Taxa de alucinação citacional (referências bibliográficas fabricadas/imprecisas)
- Coerência interna (rubrica 0–3): o raciocínio leva ao número?
- Reprodutibilidade intra-modelo (CV entre n runs)

### 2.6 Critério operacional de "concordância" (OE5)

Output é **operacionalmente concordante** quando satisfaz simultaneamente:

1. Erro relativo absoluto < 30%
2. Modelo de caracterização declarado é Oberschelp (2020) ou compatível
3. Sem alucinações citacionais
4. Coerência interna ≥ 2 (em 0–3)

---

## 3. Hipóteses confirmatórias (pré-registráveis)

| ID | Hipótese | Direção esperada |
|----|----------|------------------|
| **H1** | MAPE diminui monotonicamente com nível de prompt | Curva de saturação |
| **H2** | Salto principal de MAPE está entre L2→L3 (fornecer fatores) | Retornos decrescentes |
| **H3** | L0/L1 produz resultados indistinguíveis de "busca por valores globais genéricos" | Sim, com viés sistemático |
| **H4** | Variância entre LLMs diminui com o nível de prompt | Homogeneização por contexto |
| **H5** | Taxa de alucinação maior em L0/L1 do que em L3/L4 | Sim |
| **H6** | Modelos com cutoff > 2023 mostram viés de contaminação em L0/L1 | Atenua com inventário próprio |
| **H7** *(novo)* | Output em L0 varia em função do idioma e país-VPS | Diferença detectável > variância intra-LLM |

---

## 4. Análise estatística

- Principal: **ANOVA mista de dois fatores** (nível × modelo) sobre log-MAPE
- Backup não-paramétrico: **Friedman + post-hoc Nemenyi**
- Efeitos: η² parcial, Cohen's d
- Saturação: ajuste de função logística e exponencial saturante sobre MAPE × nível
- Múltiplos testes: **Bonferroni–Holm**
- CIs: bootstrap n = 10.000

---

## 5. Mitigação de ameaças à validade

| Ameaça | Mitigação |
|--------|-----------|
| Contaminação de treinamento (paper de 2023) | "Stress test" com inventário sintético alterado |
| Viés do experimentador na rubrica | Dupla rotulagem cega, κ ≥ 0.80 |
| Variabilidade estocástica das LLMs | T fixa, seed, n ≥ 5 |
| Drift de modelo entre piloto e principal | Registrar timestamp + versão; congelar APIs quando possível |
| Viés linguístico | Replicar PT-BR + EN (ES adiado para fase IJLCA) |
| Viés geográfico de API | Multi-VPS no L0 (BR, EU, US) |
| Generalização limitada (1 caso) | Discutir explicitamente; F3 expande para 4 sistemas × 5 modelos |

---

## 6. Orçamento esperado (F2 — evento GCV 2026)

### 6.1 Volume de outputs

| Bloco | LLMs | Idiomas | VPS | Reps | Outputs |
|-------|------|---------|-----|------|---------|
| L0 (extensão H7) | 3 | 2 (PT/EN) | 3 (BR/EU/US) | 5 | **90** |
| L1 × 3 escopos | 3 | 2 | 1 | 5 | 90 |
| L2 × 3 escopos | 3 | 2 | 1 | 5 | 90 |
| L3 × 3 escopos | 3 | 2 | 1 | 5 | 90 |
| L4 × 3 escopos | 3 | 2 | 1 | 5 | 90 |
| **Subtotal F2** | | | | | **450** |
| Buffer (re-runs, T=0.7) | | | | | ~100 |
| **Total estimado** | | | | | **~550** |

### 6.2 Custo por LLM (estimativa, ~550 outputs distribuídos)

Tokens médios: ~5.000 input + ~2.000 output por chamada.

| Modelo | $/1M in | $/1M out | Outputs | Custo |
|--------|---------|----------|---------|-------|
| GPT (4.1 ou 5) | $2.50 | $10.00 | ~183 | **~$6** |
| Gemini 2.5 Pro | $3.50 | $10.50 | ~183 | **~$7** |
| DeepSeek V3 | $0.27 | $1.10 | ~183 | **~$0.65** |
| **Total F2** | | | **550** | **~$14** |

Custo trivial. **Decisão**: orçamento não é o gargalo; tempo de orquestração e validação manual da rubrica de corretude metodológica são.

---

## 7. Decisões pendentes

- [ ] Confirmar formato de submissão GCV 2026 (resumo expandido vs. artigo completo) + data exata da chamada
- [ ] Acesso ao LCI bruto: usar dados publicados (já temos em `ACV-Sensibilidade.xlsx`) ou banco original via Yara?
- [ ] Coautores: envolver Giusti / Silva / Vieira / Fantke?
- [ ] OSF pré-registro: criar antes do piloto
- [ ] Definir hosts VPS específicos (BR/EU/US)
- [ ] Confirmar versões exatas: GPT 4.1 vs 5, Gemini 2.5 Pro vs frontier do momento

---

## 8. Próximos passos imediatos

1. ✅ Estrutura repo + ground truth extraído
2. ✅ Push GitHub privado
3. ✅ Definir modelos LLM (3 modelos) e idiomas (PT+EN)
4. 🔲 Redigir L0–L4 (PT-BR) — versão inicial para revisão metodológica com Yara
5. 🔲 Versionar prompts em EN
6. 🔲 Pré-registro OSF
7. 🔲 Piloto (~75 outputs em PT-BR) — Sistema 1, Oberschelp, Econômica
8. 🔲 Calibração de rubricas
9. 🔲 Execução principal F2
