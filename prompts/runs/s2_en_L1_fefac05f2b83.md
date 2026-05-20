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

# L1 — Scoped question (EN)

> Level L1: question scoped using ISO 14040/14044. **No** inventory data, characterization factors or calculation procedure are provided.

---

## LCA study scope

- **Functional unit**: 1 kg of fat-and-protein-corrected milk (FPCM)
- **System boundary**: cradle-to-farm gate
- **Impact category**: **human health impact of particulate matter**
- **Indicator**: DALY (Disability-Adjusted Life Years)
- **Co-products of the system**: milk, meat (cull), biofertilizer (manure)
- **Region of origin**: typical Brazilian dairy systems
- **Geographic scopes of impact assessment**: Global, Brazil, State of Paraná

## Question

Given the scope defined above, what is the **human health impact of particulate matter**, in DALY/kg FPCM, from milk production in Brazil, for each of the three geographic scopes (Global, Brazil, State of Paraná)?

Respond in the specified JSON format.

