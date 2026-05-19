# SCOPE — Escopo experimental versionado

> Documento vivo. Mudanças de escopo entram aqui antes de qualquer execução.
> Versão atual: **v0.1** (2026-05-19).

---

## 1. Fases

| Fase | Alvo | Escopo | Status |
|------|------|--------|--------|
| **F0** | Setup + ground truth | Estrutura repo + extração GT | ✅ |
| **F1** | Piloto | 1 sistema × 1 modelo × 3 escopos × 4 LLMs × 5 níveis × 5 reps PT-BR (~300) | 🔲 |
| **F2** | Evento GCV 2026 | F1 + extensão L0 multilíngue/multi-VPS (~480) | 🔲 |
| **F3** | Artigo IJLCA | 4 sistemas × 5 modelos × 3 escopos × ambas alocações × 2 idiomas | 🔲 |

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
| **L0** | Apenas pergunta geral | *"Qual é o impacto em saúde humana, em DALY/kg FPCM, da produção de leite no Brasil?"* |
| **L1** | L0 + escopo definido (UF, fronteira do sistema, categoria de impacto, região) | + especificações ISO-style |
| **L2** | L1 + inventário (LCI) bruto do Sistema 1 | "Calcule a partir destes dados" |
| **L3** | L2 + lista de fatores de caracterização disponíveis (Oberschelp 2020) | "Calcule usando estes fatores" |
| **L4** | L3 + descrição explícita do processo de cálculo, regras de regionalização e fórmulas | "Aplique este procedimento aos dados" |

**Justificativa para 5 níveis** (não 4): separar "zero context" (L0) de "scoped question" (L1) isola o efeito de simplesmente *delimitar o problema* do efeito de *fornecer dados*.

### 2.3 Modelos LLM

- **Claude** Opus 4.7 (Anthropic)
- **GPT** (versão de fronteira no momento da execução — registrar exato)
- **Gemini** (versão de fronteira)
- **Llama** ou **DeepSeek** (1 modelo aberto)

Temperatura: fixa em 0.0 e 0.7 em runs separados; seed quando suportado.

### 2.4 Extensão L0 multilíngue + multi-jurisdição

Apenas no nível **L0** (mais sensível a viés de treinamento), replicar em:

- **3 idiomas**: PT-BR, EN, ES (a confirmar — eventualmente FR/ZH)
- **3 VPS** em países diferentes: a definir (BR, EU, US?)

Hipótese: a IA pode retornar fatores diferentes em função do *país aparente* da requisição e do idioma do prompt — replicando o viés de "amostra dominante" no corpus de treinamento.

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
| Viés linguístico | Replicar PT-BR + EN (+ ES no L0) |
| Viés geográfico de API | Multi-VPS no L0 |
| Generalização limitada (1 caso) | Discutir explicitamente; F3 expande para 4 sistemas × 5 modelos |

---

## 6. Decisões pendentes

- [ ] Confirmar formato de submissão GCV 2026 (resumo expandido vs. artigo completo) + data exata da chamada
- [ ] Acesso ao LCI bruto: usar dados publicados (já temos em `ACV-Sensibilidade.xlsx`) ou banco original via Yara?
- [ ] Coautores: envolver Giusti / Silva / Vieira / Fantke?
- [ ] OSF pré-registro: criar antes do piloto
- [ ] Decidir 3º idioma (ES vs FR) e 3 países VPS

---

## 7. Próximos passos imediatos

1. ✅ Estrutura repo + ground truth extraído
2. ✅ Push GitHub privado
3. 🔲 Redigir L0–L4 (PT-BR) — versão inicial para revisão metodológica com Yara
4. 🔲 Pré-registro OSF
5. 🔲 Piloto (100 outputs) — Sistema 1, Oberschelp, Econômica, PT-BR apenas
6. 🔲 Calibração de rubricas
7. 🔲 Execução principal F2
