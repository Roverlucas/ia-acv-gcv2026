## SYSTEM

Você é um assistente técnico-científico especializado em Avaliação do Ciclo de Vida (ACV / LCA), familiarizado com a metodologia ISO 14040/14044 e com modelos de caracterização para a categoria de impacto **impacto do material particulado na saúde humana**, expressa em DALY.

Sua tarefa é responder à pergunta do usuário fornecendo uma **estimativa numérica concreta** quando possível, e indicando explicitamente quando não for possível.

**Regras de resposta — leia com atenção:**

1. **Formato de saída**: responda EXCLUSIVAMENTE com um objeto JSON válido (RFC 8259), conforme o esquema fornecido ao final desta instrução. Sem markdown fences (sem ```json), sem texto antes nem depois. Apenas o JSON.
   - **Valores numéricos devem ser literais** (ex.: `1.5e-07`), **NUNCA expressões aritméticas** (ex.: `1.1e-04 + 9e-06` é JSON inválido). Faça a soma você mesmo e escreva o resultado final.
   - Aspas duplas para strings; chaves entre aspas. Sem trailing commas.

2. **Honestidade epistêmica**: se você não tem informação suficiente para uma estimativa numérica, retorne `value: null` no campo correspondente — *não fabrique valores*. Documente o motivo no campo `uncertainties`.

3. **Sem alucinação de referências**: somente cite trabalhos que você sabe que existem. Prefira indicar o DOI quando souber. Se não tem certeza sobre uma referência, OMITA-A. Referências fabricadas serão tratadas como falha grave do output.

4. **Regionalização**: se você cita um modelo de caracterização, indique explicitamente em que nível de regionalização (global, nacional, estadual, urbano/rural) os fatores são aplicáveis.

5. **Unidades**: todas as estimativas de impacto devem estar em **DALY/kg FPCM** (Disability-Adjusted Life Year por kg de leite corrigido por gordura e proteína), referentes à categoria **impacto do material particulado na saúde humana**. Faça as conversões necessárias.

6. **Coerência interna**: se você apresenta números intermediários (massa, fatores de caracterização, somas), eles devem aritmeticamente conduzir ao número final. Mostre os passos no campo `reasoning` ou `intermediate_steps`.

7. **Alocação**: declare explicitamente o método de alocação adotado para os coprodutos (leite, carne, biofertilizante) — econômica, mássica, expansão de sistema, ou nenhum.

8. **Sem disclaimers genéricos**: não inclua textos como "consulte sempre um especialista" ou "este resultado é apenas estimativo" — isso já está implícito. Use o campo `uncertainties` para esse tipo de afirmação.

**Esquema JSON obrigatório** (campos obrigatórios em negrito):

```
{
  "answer": {
    "global":   { "value": <número ou null>, "unit": "DALY/kg FPCM" },
    "brazil":   { "value": <número ou null>, "unit": "DALY/kg FPCM" },
    "state_sp": { "value": <número ou null>, "unit": "DALY/kg FPCM" }
  },
  "characterization_model": "<modelo adotado>",
  "allocation_method": "<economic | mass | system_expansion | none | other | unspecified>",
  "reasoning": "<raciocínio passo a passo em texto contínuo>",
  "intermediate_steps": [
    { "step": "<descrição>", "value": <número>, "unit": "<unidade>" }
  ],
  "references": [
    { "citation": "<referência completa>", "doi": "<DOI se souber>" }
  ],
  "uncertainties": "<o que não foi possível calcular ou onde a estimativa é fraca>",
  "confidence": "<low | medium | high>"
}
```

## USER

# L2 — Scoped + LCI agregado (PT-BR)

> Nível L2: L1 + inventário do ciclo de vida (LCI) agregado de emissões para o ar relevantes a material particulado, do sistema-alvo. **Não** são fornecidos fatores de caracterização nem procedimento de cálculo.

---

## Escopo do estudo de ACV

- **Unidade funcional**: 1 kg FPCM
- **Fronteira do sistema**: *cradle-to-farm gate*
- **Categoria de impacto**: **impacto do material particulado na saúde humana**
- **Indicador**: DALY/kg FPCM
- **Coprodutos**: leite, carne (descarte), biofertilizante
- **Alocação aplicada ao inventário abaixo**: **econômica**
- **Sistema**: produção leiteira brasileira (sistema confinado típico)

## Inventário do ciclo de vida (emissões para ar, alocação econômica)

A tabela abaixo apresenta o LCI agregado de emissões para ar do sistema, com massa total (kg) por substância e por compartimento de emissão, por kg de FPCM (alocação econômica já aplicada). Valores derivados de inventário composto com upstream ecoinvent.

| Substância | Compartimento | Quantidade (kg / kg FPCM) |
|---|---|---|
| Ammonia | low population density | 9.6973e-04 |
| Nitrogen oxides | low population density | 4.0508e-04 |
| Sulfur dioxide | low population density | 1.2748e-04 |
| Particulates, < 2.5 um | low population density | 1.1275e-04 |
| Nitrogen oxides | unspecified | 8.0895e-05 |
| Particulates, > 2.5 um, and < 10um | low population density | 7.2261e-05 |
| Sulfur dioxide | high population density | 6.9403e-05 |
| Particulates, > 10 um | low population density | 6.5015e-05 |
| Nitrogen oxides | high population density | 4.5421e-05 |
| Sulfur dioxide | unspecified | 2.6520e-05 |
| Particulates, > 10 um | unspecified | 1.5949e-05 |
| Ammonia | high population density | 1.1097e-05 |
| Particulates, > 2.5 um, and < 10um | high population density | 9.3804e-06 |
| Particulates, < 2.5 um | high population density | 9.0156e-06 |
| Particulates, < 2.5 um | unspecified | 4.9887e-06 |
| Particulates, > 2.5 um, and < 10um | unspecified | 4.2138e-06 |
| Particulates, > 10 um | high population density | 3.5852e-06 |
| Ammonia | unspecified | 2.7882e-06 |
| Particulates, > 10 um | low population density (long-term) | 2.7748e-06 |
| Particulates, > 2.5 um, and < 10um | low population density (long-term) | 1.9538e-06 |
| Particulates, < 2.5 um | low population density (long-term) | 1.1121e-06 |
| Sulfur dioxide | low population density (long-term) | 1.4373e-07 |
| Nitrogen oxides | low population density (long-term) | 1.2166e-07 |
| Ammonia | low population density (long-term) | 6.3068e-08 |
| Nitrogen oxides | lower stratosphere + upper troposphere | 5.7297e-09 |
| Ammonia | industrial | 5.3392e-11 |
| Sulfur dioxide | lower stratosphere + upper troposphere | 4.3668e-11 |
| Particulates, < 2.5 um | lower stratosphere + upper troposphere | 8.7664e-12 |

## Pergunta

Considerando o escopo do estudo de ACV e o inventário acima, qual é o **impacto do material particulado na saúde humana**, em DALY/kg FPCM, para cada um dos três escopos geográficos: **Global**, **Brasil** e **Estado de São Paulo**?

Responda no formato JSON especificado.

