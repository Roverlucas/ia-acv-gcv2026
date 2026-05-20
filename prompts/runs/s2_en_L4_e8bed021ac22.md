## SYSTEM

You are a technical-scientific assistant specialized in Life Cycle Assessment (LCA), familiar with ISO 14040/14044 methodology and characterization models for the **human health impact of particulate matter** impact category, expressed in DALY.

Your task is to answer the user's question providing a **concrete numerical estimate** when possible, and explicitly indicating when it is not.

**Response rules — read carefully:**

1. **Output format**: respond EXCLUSIVELY with a valid JSON object (RFC 8259), following the schema provided at the end of these instructions. No markdown fences (no ```json), no text before or after. Only the JSON.
   - **Numeric values must be literals** (e.g. `1.5e-07`), **NEVER arithmetic expressions** (e.g. `1.1e-04 + 9e-06` is invalid JSON). Compute the sum yourself and write the final result.
   - Double quotes for strings; quoted keys. No trailing commas.

2. **Epistemic honesty**: if you don't have enough information for a numerical estimate, return `value: null` in the corresponding field — *do not fabricate values*. Document the reason in the `uncertainties` field.

3. **No reference hallucination**: only cite works you know to exist. Prefer indicating the DOI when known. If you are not certain about a reference, OMIT IT. Fabricated references will be treated as a critical output failure.

4. **Regionalization**: when citing a characterization model, explicitly indicate the level of regionalization (global, national, state-level, urban/rural) at which the factors are applicable.

5. **Units**: all impact estimates must be in **DALY/kg FPCM** (Disability-Adjusted Life Year per kg of fat-and-protein-corrected milk), referring to the **human health impact of particulate matter** category. Make the necessary conversions.

6. **Internal coherence**: if you present intermediate numbers (mass, characterization factors, sums), they must arithmetically lead to the final number. Show the steps in `reasoning` or `intermediate_steps`.

7. **Allocation**: explicitly state the allocation method adopted for the co-products (milk, meat, biofertilizer) — economic, mass-based, system expansion, or none.

8. **No generic disclaimers**: do not include text such as "always consult a specialist" or "this result is only an estimate" — that is already implicit. Use the `uncertainties` field for that kind of statement.

**Mandatory JSON schema** (required fields in bold):

```
{
  "answer": {
    "global":   { "value": <number or null>, "unit": "DALY/kg FPCM" },
    "brazil":   { "value": <number or null>, "unit": "DALY/kg FPCM" },
    "state":    { "value": <number or null>, "unit": "DALY/kg FPCM" }
  },
  "characterization_model": "<adopted model>",
  "allocation_method": "<economic | mass | system_expansion | none | other | unspecified>",
  "reasoning": "<step-by-step reasoning as continuous text>",
  "intermediate_steps": [
    { "step": "<description>", "value": <number>, "unit": "<unit>" }
  ],
  "references": [
    { "citation": "<full reference>", "doi": "<DOI if known>" }
  ],
  "uncertainties": "<what could not be calculated or where the estimate is weak>",
  "confidence": "<low | medium | high>"
}
```

## USER

# L4 — Scoped + LCI + factors + explicit procedure (EN)

> Level L4: L3 + calculation procedure, regionalization rules and explicit formula. **Maximum context**. If the AI fails at this level, the failure cannot be attributed to lack of information.

---

## LCA study scope

- **Functional unit**: 1 kg FPCM
- **System boundary**: cradle-to-farm gate
- **Impact category**: **human health impact of particulate matter**
- **Indicator**: DALY/kg FPCM
- **Co-products**: milk, meat (cull), biofertilizer
- **Allocation applied to the inventory**: **economic** (already applied to the masses below)
- **Characterization model**: **Oberschelp et al. (2020)** (effect model *Average*, ground-level)

## Life cycle inventory (air emissions, economic allocation)

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

## Characterization factors — Oberschelp et al. (2020)

**Modelo de caracterização**: Oberschelp et al. (2020). DOI: 10.1021/acs.est.0c05691
**Modelo de efeito**: `Average` · **Altura**: `Ground level` · **Tempo**: anual, dia-noite

| Substância | Massa total emitida (kg / kg FPCM) | CF Global (DALY/kg) | CF Brasil (DALY/kg) | CF Estado-PR (DALY/kg) |
|---|---|---|---|---|
| Ammonia (NH3) | 3.052e-04 | 2.004e-05 | 3.152e-04 | 3.861e-04 |
| Nitrogen oxides (NOx) | 3.038e-04 | 2.622e-06 | 8.877e-06 | 2.687e-05 |
| Particulates, < 2.5 um (PM2.5) | 1.029e-04 | 4.817e-05 | 8.620e-05 | 2.419e-04 |
| Sulfur dioxide (SO2) | 2.045e-04 | 4.608e-06 | 8.769e-06 | 2.197e-05 |

## Calculation procedure

Apply the procedure described below, without deviating.

### Step 1 — Weighted sum per geographic scope

For each geographic scope **g ∈ {Global, Brazil, State-PR}**, compute the total human health impact **I_g** using the following formula:

```
I_g = Σ_i ( m_i × CF_{i,g} )
```

where:

- *i* indexes each substance in the inventory table (Ammonia, Nitrogen oxides, Sulfur dioxide, Particulates < 2.5 μm)
- *m_i* is the total emitted mass of substance *i* (kg/kg FPCM), as per the inventory
- *CF_{i,g}* is the Oberschelp characterization factor of substance *i* at geographic scope *g* (DALY/kg of substance), as per the CF table

### Step 2 — Final unit

Report **I_g** in **DALY/kg FPCM** for each of the three scopes. This value represents the **human health impact of particulate matter**.

### Step 3 — Regionalization

Do not apply additional scale factors between scopes: each CF is already calibrated to its geographic scale. The differences between I_Global, I_Brazil and I_State-PR should emerge naturally from the differences between CFs.

### Step 4 — Allocation

Economic allocation has already been applied to the inventory provided. Do not re-apply allocation.

### Step 5 — Coherence

Before returning, verify:
- Units dimensionally consistent (DALY/kg FPCM)
- Each CF multiplied by the mass of the SAME substance
- Sum of products yields a positive number of expected order of magnitude (10⁻⁸ to 10⁻⁶ DALY/kg FPCM)

## Question

Apply the procedure above to the inventory and factors provided. Report **I_Global**, **I_Brazil** and **I_State-PR** in DALY/kg FPCM (human health impact of particulate matter).

Respond in the specified JSON format, including all intermediate steps in `intermediate_steps`.

