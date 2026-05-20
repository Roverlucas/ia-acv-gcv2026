# Regional differentiation analysis


## Criteria

- **Differentiates**: pairwise relative difference between scopes >= 1% in at least one pair.

- **Monotonic**: global <= brazil <= state (expected for milk-system regionalization).

- **State/Global ratio**: ratio reported by LLM vs published GT.


## Aggregated results


|   system | provider   | level   |   n |   share_differentiates |   share_monotonic |   median_ratio_state_global |   median_log10_ratio_diff |
|---------:|:-----------|:--------|----:|-----------------------:|------------------:|----------------------------:|--------------------------:|
|        1 | deepseek   | L0      |  10 |                      1 |              1    |                       1.583 |                    -1.154 |
|        1 | deepseek   | L1      |  10 |                      1 |              0.9  |                       1.5   |                    -1.176 |
|        1 | deepseek   | L2      |   7 |                      0 |              1    |                       1     |                    -1.353 |
|        1 | deepseek   | L3      |  24 |                      1 |              1    |                      20.312 |                    -0.045 |
|        1 | deepseek   | L4      |  24 |                      1 |              1    |                      20.638 |                    -0.038 |
|        1 | gemini     | L0      |   5 |                      1 |              1    |                       1.87  |                    -1.081 |
|        1 | gemini     | L1      |   2 |                      1 |              1    |                       3.046 |                    -0.869 |
|        1 | gemini     | L2      |   2 |                      1 |              1    |                       1.134 |                    -1.298 |
|        1 | gemini     | L3      |  25 |                      1 |              1    |                      22.523 |                     0     |
|        1 | gemini     | L4      |  25 |                      1 |              1    |                      22.523 |                     0     |
|        1 | gpt        | L0      |   4 |                      1 |              0.75 |                       1.467 |                    -1.186 |
|        1 | gpt        | L1      |   3 |                      1 |              0    |                       0.48  |                    -1.671 |
|        1 | gpt        | L3      |  25 |                      1 |              1    |                      25.537 |                     0.055 |
|        1 | gpt        | L4      |  25 |                      1 |              1    |                      25.531 |                     0.054 |