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
|        2 | deepseek   | L0      |   5 |                      1 |              0.6  |                       1.5   |                    -0.908 |
|        2 | deepseek   | L1      |  10 |                      1 |              0.9  |                       1.583 |                    -0.885 |
|        2 | deepseek   | L2      |   8 |                      0 |              1    |                       1     |                    -1.084 |
|        2 | deepseek   | L3      |   9 |                      1 |              1    |                      13.333 |                     0.041 |
|        2 | deepseek   | L4      |   9 |                      1 |              1    |                      11.963 |                    -0.006 |
|        2 | gemini     | L0      |   2 |                      1 |              0.5  |                       1.229 |                    -1.05  |
|        2 | gemini     | L1      |   1 |                      1 |              1    |                       1.081 |                    -1.05  |
|        2 | gemini     | L2      |   1 |                      1 |              1    |                       1.165 |                    -1.017 |
|        2 | gemini     | L3      |  10 |                      1 |              1    |                      12.131 |                     0     |
|        2 | gemini     | L4      |  10 |                      1 |              1    |                      12.128 |                     0     |
|        2 | gpt        | L3      |  15 |                      1 |              1    |                      19.287 |                     0.202 |
|        2 | gpt        | L4      |  15 |                      1 |              1    |                      19.778 |                     0.212 |