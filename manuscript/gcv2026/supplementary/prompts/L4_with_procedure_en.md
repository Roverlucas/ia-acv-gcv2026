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

{{LCI_TABLE}}

## Characterization factors — Oberschelp et al. (2020)

{{CF_TABLE_OBERSCHELP}}

## Calculation procedure

Apply the procedure described below, without deviating.

### Step 1 — Weighted sum per geographic scope

For each geographic scope **g ∈ {Global, Brazil, State-{{STATE_CODE}}}**, compute the total human health impact **I_g** using the following formula:

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

Do not apply additional scale factors between scopes: each CF is already calibrated to its geographic scale. The differences between I_Global, I_Brazil and I_State-{{STATE_CODE}} should emerge naturally from the differences between CFs.

### Step 4 — Allocation

Economic allocation has already been applied to the inventory provided. Do not re-apply allocation.

### Step 5 — Coherence

Before returning, verify:
- Units dimensionally consistent (DALY/kg FPCM)
- Each CF multiplied by the mass of the SAME substance
- Sum of products yields a positive number of expected order of magnitude (10⁻⁸ to 10⁻⁶ DALY/kg FPCM)

## Question

Apply the procedure above to the inventory and factors provided. Report **I_Global**, **I_Brazil** and **I_State-{{STATE_CODE}}** in DALY/kg FPCM (human health impact of particulate matter).

Respond in the specified JSON format, including all intermediate steps in `intermediate_steps`.
