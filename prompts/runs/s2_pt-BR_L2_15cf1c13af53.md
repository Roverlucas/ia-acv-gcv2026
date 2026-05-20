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
    "state":    { "value": <número ou null>, "unit": "DALY/kg FPCM" }
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
| Ammonia | low population density | 3.0111e-04 |
| Nitrogen oxides | low population density | 2.0721e-04 |
| Sulfur dioxide | low population density | 1.0258e-04 |
| Particulates, < 2.5 um | low population density | 9.1741e-05 |
| Sulfur dioxide | high population density | 8.8345e-05 |
| Particulates, > 2.5 um, and < 10um | low population density | 5.9490e-05 |
| Nitrogen oxides | high population density | 5.4653e-05 |
| Particulates, > 10 um | low population density | 4.7238e-05 |
| Nitrogen oxides | unspecified | 4.1960e-05 |
| Sulfur dioxide | unspecified | 1.3527e-05 |
| Particulates, > 10 um | unspecified | 9.7557e-06 |
| Particulates, < 2.5 um | high population density | 8.1504e-06 |
| Particulates, > 2.5 um, and < 10um | high population density | 3.9159e-06 |
| Ammonia | high population density | 2.8134e-06 |
| Particulates, < 2.5 um | unspecified | 2.7487e-06 |
| Particulates, > 10 um | high population density | 2.6992e-06 |
| Particulates, > 2.5 um, and < 10um | unspecified | 2.2041e-06 |
| Ammonia | unspecified | 1.2391e-06 |
| Particulates, > 10 um | low population density (long-term) | 6.5960e-07 |
| Particulates, > 2.5 um, and < 10um | low population density (long-term) | 4.5352e-07 |
| Particulates, < 2.5 um | low population density (long-term) | 2.6443e-07 |
| Sulfur dioxide | low population density (long-term) | 4.3861e-08 |
| Nitrogen oxides | low population density (long-term) | 2.1007e-08 |
| Nitrogen oxides | lower stratosphere + upper troposphere | 2.1979e-09 |
| Ammonia | low population density (long-term) | 6.5822e-10 |
| Ammonia | industrial | 1.9079e-11 |
| Sulfur dioxide | lower stratosphere + upper troposphere | 1.4220e-11 |
| Particulates, < 2.5 um | lower stratosphere + upper troposphere | 2.8546e-12 |

## Pergunta

Considerando o escopo do estudo de ACV e o inventário acima, qual é o **impacto do material particulado na saúde humana**, em DALY/kg FPCM, para cada um dos três escopos geográficos: **Global**, **Brasil** e **Estado do Paraná**?

Responda no formato JSON especificado.

