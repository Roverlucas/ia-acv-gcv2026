# Prompts — Design experimental L0 → L4

Cada nível adiciona **uma única dimensão de informação** ao anterior. O objetivo é localizar empiricamente onde o ganho de assertividade ocorre.

| Nível | Adiciona | O que a IA ainda precisa fornecer | Token cost típico |
|-------|----------|-----------------------------------|-------------------|
| **L0** | (nada — pergunta genérica) | Tudo: escopo, dados, fatores, procedimento | ~200 in / ~800 out |
| **L1** | Escopo ISO-style (UF, fronteira, categoria, região) | Dados, fatores, procedimento | ~500 in / ~1.000 out |
| **L2** | LCI agregado (28 fluxos PM-relevantes do Sistema 1) | Fatores e procedimento | ~3.500 in / ~1.500 out |
| **L3** | Fatores de caracterização Oberschelp (Global/Brasil/SP) | Procedimento de cálculo e regionalização | ~5.500 in / ~2.000 out |
| **L4** | Procedimento explícito (fórmula, regras de regionalização, alocação) | Apenas executar | ~7.500 in / ~3.000 out |

## Princípios de design

1. **Pergunta-alvo constante**: a mesma pergunta em todos os níveis. Muda apenas o **contexto entregue**.
2. **Output estruturado**: JSON estrito, esquema único em todos os níveis — comparável ponto a ponto contra o ground truth.
3. **Reasoning visível**: campo `reasoning` obrigatório → permite rubrica D (coerência interna 0–3).
4. **Citações verificáveis**: campo `references[]` permite rubrica D (alucinação citacional).
5. **Sem cues sobre a resposta**: o prompt nunca menciona o valor esperado nem expressões como "regionalize cuidadosamente" — isso seria *priming*.
6. **Antiviés metodológico**: o prompt **não** força modelo de caracterização (exceto L3/L4 onde fatores específicos são dados). A IA pode escolher Fantke, Van Zelm, etc. em L0/L1/L2 — esse é o achado.

## Anatomia de um prompt

```
[ system_instruction ] (comum a todos os níveis e idiomas)
[ level_specific_context ] (vazio em L0; cresce em L1→L4)
[ user_question ] (constante: pergunta-alvo)
[ output_schema ] (mesmo JSON em todos os níveis)
```

## Pergunta-alvo (constante em PT-BR)

> Em um estudo de ACV de produção de leite no Brasil, qual é o **impacto do material particulado na saúde humana**, em DALY/kg FPCM? Forneça uma estimativa para escopo **Global**, **Brasil** e **Estado de São Paulo**.

## Arquivos

```
templates/
├── README.md                       # este arquivo
├── _system_instruction_pt.md       # instrução de sistema (PT-BR)
├── _system_instruction_en.md       # instrução de sistema (EN)
├── _response_schema.json           # JSON Schema do output
├── pt-BR/
│   ├── L0_zero_context.md
│   ├── L1_scoped.md
│   ├── L2_with_lci.md              # injeta {{LCI_TABLE}}
│   ├── L3_with_factors.md          # injeta {{LCI_TABLE}} + {{CF_TABLE_OBERSCHELP}}
│   └── L4_with_procedure.md        # idem L3 + procedimento explícito
└── en/                             # tradução literal a partir do PT
    └── ...
```

## Convenção de placeholders

Trechos entre `{{...}}` são substituídos pelo orquestrador de execução (`src/run_experiment.py`, a criar) com dados de `data/processed/`. Versão final do prompt executado é salva em `prompts/runs/<run_id>.md` para auditoria.

| Placeholder | Origem |
|-------------|--------|
| `{{LCI_TABLE}}` | `data/processed/sistema1_emissions_air_pm.md` |
| `{{CF_TABLE_OBERSCHELP}}` | `data/processed/cf_oberschelp_s1.md` (a gerar) |
| `{{LANGUAGE}}` | `pt-BR` ou `en` |

## Versionamento

Cada commit em `prompts/templates/` deve incluir o hash do conteúdo no commit message. Prompts são **read-only após o pré-registro OSF**. Mudanças retrospectivas exigem nova versão (L0v2, etc.) e relato explícito.
