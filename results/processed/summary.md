# Aggregated results


## MAPE by (LLM × level × language)


|                    |      en |   pt-BR |
|:-------------------|--------:|--------:|
| ('deepseek', 'L0') |   20.24 |    2.13 |
| ('deepseek', 'L1') |   20.24 |   89.43 |
| ('deepseek', 'L2') | 2017.92 |    2.16 |
| ('deepseek', 'L3') |    0.15 |    0.32 |
| ('deepseek', 'L4') |    0.05 |    0.05 |
| ('gemini', 'L0')   |   16.86 |    5.78 |
| ('gemini', 'L1')   |  110.04 |  273.25 |
| ('gemini', 'L2')   |    0.65 |    2.6  |
| ('gemini', 'L3')   |    0    |    0    |
| ('gemini', 'L4')   |    0    |    0    |
| ('gpt', 'L0')      |    2.45 |    2.49 |
| ('gpt', 'L1')      |  nan    |    3.94 |
| ('gpt', 'L2')      |  nan    |  nan    |
| ('gpt', 'L3')      |    0.17 |    0.2  |
| ('gpt', 'L4')      |    0.07 |    0.11 |


## Aggregated table


| provider   | level   | language   | geo_scope   |   n_total |   n_responded |      mape |   median_abs_rel_error |   median_log_ratio |   cv_estimate |   share_within_30 |
|:-----------|:--------|:-----------|:------------|----------:|--------------:|----------:|-----------------------:|-------------------:|--------------:|------------------:|
| deepseek   | L0      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |               0   |
| deepseek   | L0      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |               0   |
| deepseek   | L0      | en         | state_sp    |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |               0   |
| deepseek   | L0      | pt-BR      | brazil      |         5 |             5 |    1.4668 |                 1.4668 |             0.3921 |        0      |               0   |
| deepseek   | L0      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |               0   |
| deepseek   | L0      | pt-BR      | state_sp    |         5 |             5 |    0.6077 |                 0.6077 |            -0.4064 |        0      |               0   |
| deepseek   | L1      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |               0   |
| deepseek   | L1      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |               0   |
| deepseek   | L1      | en         | state_sp    |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |               0   |
| deepseek   | L1      | pt-BR      | brazil      |         5 |             5 |   77.4938 |                17.501  |             1.2672 |        1.1107 |               0   |
| deepseek   | L1      | pt-BR      | global      |         5 |             5 |  179.228  |                41.4066 |             1.6274 |        1.1072 |               0   |
| deepseek   | L1      | pt-BR      | state_sp    |         5 |             5 |   11.5532 |                 1.8245 |             0.4509 |        1.1124 |               0   |
| deepseek   | L2      | en         | brazil      |         5 |             4 | 1516.09   |              1516.09   |             3.181  |        0      |               0   |
| deepseek   | L2      | en         | global      |         5 |             4 | 4345.68   |              4345.68   |             3.6382 |        0      |               0   |
| deepseek   | L2      | en         | state_sp    |         5 |             4 |  192.01   |               192.01   |             2.2856 |        0      |               0   |
| deepseek   | L2      | pt-BR      | brazil      |         5 |             5 |    0.8501 |                 0.8501 |             0.2672 |        0      |               0   |
| deepseek   | L2      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |               0   |
| deepseek   | L2      | pt-BR      | state_sp    |         5 |             3 |    0.7646 |                 0.7646 |            -0.6282 |        0      |               0   |
| deepseek   | L3      | en         | brazil      |         5 |             5 |    0.0715 |                 0.0953 |             0.0395 |        0.0348 |               1   |
| deepseek   | L3      | en         | global      |         5 |             5 |    0.3499 |                 0.3499 |             0.1303 |        0      |               0   |
| deepseek   | L3      | en         | state_sp    |         5 |             5 |    0.0258 |                 0.0294 |             0.0032 |        0.0276 |               1   |
| deepseek   | L3      | pt-BR      | brazil      |         5 |             4 |    0.2735 |                 0.2581 |             0.0997 |        0.021  |               0.6 |
| deepseek   | L3      | pt-BR      | global      |         5 |             4 |    0.4418 |                 0.4418 |             0.1589 |        0      |               0   |
| deepseek   | L3      | pt-BR      | state_sp    |         5 |             4 |    0.2412 |                 0.2271 |             0.0889 |        0.0197 |               0.8 |
| deepseek   | L4      | en         | brazil      |         5 |             5 |    0.0442 |                 0.0527 |            -0.0235 |        0.0321 |               1   |
| deepseek   | L4      | en         | global      |         5 |             5 |    0.0178 |                 0.0178 |             0.0076 |        0      |               1   |
| deepseek   | L4      | en         | state_sp    |         5 |             5 |    0.0754 |                 0.0867 |            -0.0394 |        0.0244 |               1   |
| deepseek   | L4      | pt-BR      | brazil      |         5 |             5 |    0.0493 |                 0.0527 |            -0.0235 |        0.0073 |               1   |
| deepseek   | L4      | pt-BR      | global      |         5 |             5 |    0.0246 |                 0.0211 |            -0.0093 |        0.0072 |               1   |
| deepseek   | L4      | pt-BR      | state_sp    |         5 |             5 |    0.082  |                 0.0867 |            -0.0394 |        0.0103 |               1   |
| gemini     | L0      | en         | brazil      |         5 |             5 |   14.8887 |                10.261  |             1.0516 |        0.5521 |               0   |
| gemini     | L0      | en         | global      |         5 |             5 |   33.5331 |                25.0801 |             1.4163 |        0.5154 |               0   |
| gemini     | L0      | en         | state_sp    |         5 |             5 |    2.1691 |                 2.3722 |             0.5279 |        0.1589 |               0   |
| gemini     | L0      | pt-BR      | brazil      |         5 |             5 |    3.2427 |                 0.1367 |            -0.0639 |        1.6273 |               0.6 |
| gemini     | L0      | pt-BR      | global      |         5 |             5 |    8.3215 |                 2.5339 |             0.5483 |        1.3806 |               0.2 |
| gemini     | L0      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gemini     | L1      | en         | brazil      |         5 |             5 |   80.9769 |                22.6813 |             1.3744 |        1.0951 |               0   |
| gemini     | L1      | en         | global      |         5 |             5 |  182.929  |                91.5878 |             1.9666 |        1.0177 |               0   |
| gemini     | L1      | en         | state_sp    |         5 |             2 |    0.4837 |                 0.4837 |            -0.2871 |        0      |               0   |
| gemini     | L1      | pt-BR      | brazil      |         5 |             4 |  175.451  |                21.5959 |             1.354  |        1.5416 |               0   |
| gemini     | L1      | pt-BR      | global      |         5 |             5 |  351.484  |                35.399  |             1.5611 |        1.781  |               0   |
| gemini     | L1      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gemini     | L2      | en         | brazil      |         5 |             5 |    0.4413 |                 0.4549 |            -0.2635 |        0.3761 |               0.2 |
| gemini     | L2      | en         | global      |         5 |             5 |    0.7507 |                 0.3778 |             0.1392 |        0.3315 |               0.2 |
| gemini     | L2      | en         | state_sp    |         5 |             2 |    0.9306 |                 0.9306 |            -1.159  |        0      |               0   |
| gemini     | L2      | pt-BR      | brazil      |         5 |             5 |    1.3405 |                 0.6946 |            -0.5152 |        1.5287 |               0   |
| gemini     | L2      | pt-BR      | global      |         5 |             5 |    3.8551 |                 0.5649 |             0.1945 |        1.3685 |               0   |
| gemini     | L2      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gemini     | L3      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |               1   |
| gemini     | L3      | en         | global      |         5 |             5 |    0      |                 0.0001 |             0      |        0      |               1   |
| gemini     | L3      | en         | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |               1   |
| gemini     | L3      | pt-BR      | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |               1   |
| gemini     | L3      | pt-BR      | global      |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0      |               1   |
| gemini     | L3      | pt-BR      | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |               1   |
| gemini     | L4      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |               1   |
| gemini     | L4      | en         | global      |         5 |             5 |    0      |                 0      |             0      |        0      |               1   |
| gemini     | L4      | en         | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |               1   |
| gemini     | L4      | pt-BR      | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |               1   |
| gemini     | L4      | pt-BR      | global      |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0      |               1   |
| gemini     | L4      | pt-BR      | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |               1   |
| gpt        | L0      | en         | brazil      |         5 |             5 |    1.0721 |                 0.8501 |             0.2672 |        0.4027 |               0   |
| gpt        | L0      | en         | global      |         5 |             5 |    4.1595 |                 3.2407 |             0.6274 |        0.3562 |               0   |
| gpt        | L0      | en         | state_sp    |         5 |             1 |    0.8274 |                 0.8274 |            -0.7629 |        0      |               0   |
| gpt        | L0      | pt-BR      | brazil      |         5 |             5 |    1.0721 |                 1.4668 |             0.3921 |        0.2333 |               0   |
| gpt        | L0      | pt-BR      | global      |         5 |             5 |    5.0076 |                 4.3008 |             0.7243 |        0.1441 |               0   |
| gpt        | L0      | pt-BR      | state_sp    |         5 |             3 |    0.6548 |                 0.6548 |            -0.4619 |        0      |               0   |
| gpt        | L1      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L1      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L1      | en         | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L1      | pt-BR      | brazil      |         5 |             5 |    1.9108 |                 1.2201 |             0.3464 |        0.2906 |               0   |
| gpt        | L1      | pt-BR      | global      |         5 |             5 |    7.8347 |                 7.8347 |             0.9462 |        0      |               0   |
| gpt        | L1      | pt-BR      | state_sp    |         5 |             3 |    0.8117 |                 0.8117 |            -0.7251 |        0      |               0   |
| gpt        | L2      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L2      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L2      | en         | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L2      | pt-BR      | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L2      | pt-BR      | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L2      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |               0   |
| gpt        | L3      | en         | brazil      |         5 |             5 |    0.2072 |                 0.2164 |             0.0851 |        0.1877 |               1   |
| gpt        | L3      | en         | global      |         5 |             5 |    0.0862 |                 0.0862 |             0.0359 |        0      |               1   |
| gpt        | L3      | en         | state_sp    |         5 |             5 |    0.2296 |                 0.2317 |             0.0905 |        0.2106 |               1   |
| gpt        | L3      | pt-BR      | brazil      |         5 |             5 |    0.2472 |                 0.2472 |             0.0959 |        0      |               1   |
| gpt        | L3      | pt-BR      | global      |         5 |             5 |    0.0862 |                 0.0862 |             0.0359 |        0      |               1   |
| gpt        | L3      | pt-BR      | state_sp    |         5 |             5 |    0.2598 |                 0.264  |             0.1018 |        0.0042 |               1   |
| gpt        | L4      | en         | brazil      |         5 |             5 |    0.0702 |                 0.0398 |            -0.006  |        0.0817 |               1   |
| gpt        | L4      | en         | global      |         5 |             5 |    0.086  |                 0.0727 |            -0.0328 |        0.0197 |               1   |
| gpt        | L4      | en         | state_sp    |         5 |             5 |    0.0686 |                 0.0537 |             0.0001 |        0.0819 |               1   |
| gpt        | L4      | pt-BR      | brazil      |         5 |             5 |    0.1502 |                 0.141  |            -0.066  |        0.1565 |               1   |
| gpt        | L4      | pt-BR      | global      |         5 |             5 |    0.032  |                 0.0364 |            -0.0161 |        0.0092 |               1   |
| gpt        | L4      | pt-BR      | state_sp    |         5 |             5 |    0.1564 |                 0.1295 |            -0.0603 |        0.1678 |               1   |