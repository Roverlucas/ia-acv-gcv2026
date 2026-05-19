# L4 — Scoped + LCI + fatores + procedimento explícito (PT-BR)

> Nível L4: L3 + procedimento de cálculo, regras de regionalização e fórmula explícita. **Máximo contexto**. Se a IA falhar neste nível, a falha não pode ser atribuída a falta de informação.

---

## Escopo do estudo de ACV

- **Unidade funcional**: 1 kg FPCM
- **Fronteira do sistema**: *cradle-to-farm gate*
- **Categoria de impacto**: **impacto do material particulado na saúde humana**
- **Indicador**: DALY/kg FPCM
- **Coprodutos**: leite, carne (descarte), biofertilizante
- **Alocação aplicada ao inventário**: **econômica** (já aplicada nas massas abaixo)
- **Modelo de caracterização**: **Oberschelp et al. (2020)** (modelo de efeito *Average*, ground-level)

## Inventário do ciclo de vida (emissões para ar, alocação econômica)

{{LCI_TABLE}}

## Fatores de caracterização — Oberschelp et al. (2020)

{{CF_TABLE_OBERSCHELP}}

## Procedimento de cálculo

Aplique o procedimento descrito abaixo, sem desviar.

### Passo 1 — Soma ponderada por escopo geográfico

Para cada escopo geográfico **g ∈ {Global, Brasil, Estado-SP}**, calcule o impacto total em saúde humana **I_g** pela seguinte fórmula:

```
I_g = Σ_i ( m_i × CF_{i,g} )
```

onde:

- *i* indexa cada substância da tabela de inventário (Ammonia, Nitrogen oxides, Sulfur dioxide, Particulates < 2.5 μm)
- *m_i* é a massa total emitida da substância *i* (kg/kg FPCM), conforme inventário
- *CF_{i,g}* é o fator de caracterização Oberschelp da substância *i* no escopo geográfico *g* (DALY/kg de substância), conforme tabela de fatores

### Passo 2 — Unidade final

Reporte **I_g** em **DALY/kg FPCM** para cada um dos três escopos. Este valor representa o **impacto do material particulado na saúde humana**.

### Passo 3 — Regionalização

Não aplique fatores de escala adicionais entre os escopos: cada CF já está calibrado para sua escala geográfica. A diferença entre I_Global, I_Brasil e I_Estado-SP deve emergir naturalmente das diferenças entre os CFs.

### Passo 4 — Alocação

A alocação econômica já foi aplicada ao inventário fornecido. Não reaplique alocação.

### Passo 5 — Coerência

Verifique antes de retornar:
- Unidades dimensionalmente consistentes (DALY/kg FPCM)
- Cada CF foi multiplicado pela massa correspondente da MESMA substância
- A soma dos produtos resulta em um número positivo da ordem esperada (10⁻⁸ a 10⁻⁶ DALY/kg FPCM)

## Pergunta

Aplique o procedimento acima ao inventário e aos fatores fornecidos. Reporte **I_Global**, **I_Brasil** e **I_Estado-SP** em DALY/kg FPCM (impacto do material particulado na saúde humana).

Responda no formato JSON especificado, incluindo todos os passos intermediários em `intermediate_steps`.
