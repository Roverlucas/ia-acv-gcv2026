# Aggregated results


## MAPE by (LLM × level × language)


|                    |      en |   pt-BR |
|:-------------------|--------:|--------:|
| ('deepseek', 'L0') |   20.24 |    2.13 |
| ('deepseek', 'L1') |   20.24 |   89.43 |
| ('deepseek', 'L2') | 2017.92 |    2.16 |
| ('deepseek', 'L3') |    0.15 |   17.62 |
| ('deepseek', 'L4') |    0.05 |    0.2  |
| ('gemini', 'L0')   |   16.86 |    5.78 |
| ('gemini', 'L1')   |  110.04 |  273.25 |
| ('gemini', 'L2')   |    0.65 |    2.6  |
| ('gemini', 'L3')   |    0    |    0.03 |
| ('gemini', 'L4')   |    0    |    0    |
| ('gpt', 'L0')      |    3.73 |    2.91 |
| ('gpt', 'L1')      |  nan    |    4.08 |
| ('gpt', 'L2')      |  nan    |  nan    |
| ('gpt', 'L3')      |    0.19 |    0.32 |
| ('gpt', 'L4')      |    0.3  |    0.24 |


## Aggregated table


| provider   | level   | language   | geo_scope   |   n_total |   n_responded |      mape |   median_abs_rel_error |   median_log_ratio |   cv_estimate |   share_within_30 |
|:-----------|:--------|:-----------|:------------|----------:|--------------:|----------:|-----------------------:|-------------------:|--------------:|------------------:|
| deepseek   | L0      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |             0     |
| deepseek   | L0      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |             0     |
| deepseek   | L0      | en         | state_sp    |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |             0     |
| deepseek   | L0      | pt-BR      | brazil      |         5 |             5 |    1.4668 |                 1.4668 |             0.3921 |        0      |             0     |
| deepseek   | L0      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |             0     |
| deepseek   | L0      | pt-BR      | state_sp    |         5 |             5 |    0.6077 |                 0.6077 |            -0.4064 |        0      |             0     |
| deepseek   | L1      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |             0     |
| deepseek   | L1      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |             0     |
| deepseek   | L1      | en         | state_sp    |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |             0     |
| deepseek   | L1      | pt-BR      | brazil      |         5 |             5 |   77.4938 |                17.501  |             1.2672 |        1.1107 |             0     |
| deepseek   | L1      | pt-BR      | global      |         5 |             5 |  179.228  |                41.4066 |             1.6274 |        1.1072 |             0     |
| deepseek   | L1      | pt-BR      | state_sp    |         5 |             5 |   11.5532 |                 1.8245 |             0.4509 |        1.1124 |             0     |
| deepseek   | L2      | en         | brazil      |         5 |             4 | 1516.09   |              1516.09   |             3.181  |        0      |             0     |
| deepseek   | L2      | en         | global      |         5 |             4 | 4345.68   |              4345.68   |             3.6382 |        0      |             0     |
| deepseek   | L2      | en         | state_sp    |         5 |             4 |  192.01   |               192.01   |             2.2856 |        0      |             0     |
| deepseek   | L2      | pt-BR      | brazil      |         5 |             5 |    0.8501 |                 0.8501 |             0.2672 |        0      |             0     |
| deepseek   | L2      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |             0     |
| deepseek   | L2      | pt-BR      | state_sp    |         5 |             3 |    0.7646 |                 0.7646 |            -0.6282 |        0      |             0     |
| deepseek   | L3      | en         | brazil      |         5 |             5 |    0.0715 |                 0.0953 |             0.0395 |        0.0348 |             1     |
| deepseek   | L3      | en         | global      |         5 |             5 |    0.3499 |                 0.3499 |             0.1303 |        0      |             0     |
| deepseek   | L3      | en         | state_sp    |         5 |             5 |    0.0258 |                 0.0294 |             0.0032 |        0.0276 |             1     |
| deepseek   | L3      | pt-BR      | brazil      |        20 |            19 |   16.3749 |                 0.2193 |             0.0859 |        3.9698 |             0.65  |
| deepseek   | L3      | pt-BR      | global      |        20 |            19 |   20.6738 |                 0.3499 |             0.1303 |        4.0144 |             0.45  |
| deepseek   | L3      | pt-BR      | state_sp    |        20 |            19 |   15.8196 |                 0.2264 |             0.0742 |        3.968  |             0.75  |
| deepseek   | L4      | en         | brazil      |         5 |             5 |    0.0442 |                 0.0527 |            -0.0235 |        0.0321 |             1     |
| deepseek   | L4      | en         | global      |         5 |             5 |    0.0178 |                 0.0178 |             0.0076 |        0      |             1     |
| deepseek   | L4      | en         | state_sp    |         5 |             5 |    0.0754 |                 0.0867 |            -0.0394 |        0.0244 |             1     |
| deepseek   | L4      | pt-BR      | brazil      |        20 |            19 |    0.1887 |                 0.0527 |            -0.0235 |        0.4611 |             0.9   |
| deepseek   | L4      | pt-BR      | global      |        20 |            19 |    0.1882 |                 0.0211 |            -0.0093 |        0.5589 |             0.85  |
| deepseek   | L4      | pt-BR      | state_sp    |        20 |            19 |    0.2135 |                 0.0867 |            -0.0394 |        0.4544 |             0.9   |
| gemini     | L0      | en         | brazil      |         5 |             5 |   14.8887 |                10.261  |             1.0516 |        0.5521 |             0     |
| gemini     | L0      | en         | global      |         5 |             5 |   33.5331 |                25.0801 |             1.4163 |        0.5154 |             0     |
| gemini     | L0      | en         | state_sp    |         5 |             5 |    2.1691 |                 2.3722 |             0.5279 |        0.1589 |             0     |
| gemini     | L0      | pt-BR      | brazil      |         5 |             5 |    3.2427 |                 0.1367 |            -0.0639 |        1.6273 |             0.6   |
| gemini     | L0      | pt-BR      | global      |         5 |             5 |    8.3215 |                 2.5339 |             0.5483 |        1.3806 |             0.2   |
| gemini     | L0      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gemini     | L1      | en         | brazil      |         5 |             5 |   80.9769 |                22.6813 |             1.3744 |        1.0951 |             0     |
| gemini     | L1      | en         | global      |         5 |             5 |  182.929  |                91.5878 |             1.9666 |        1.0177 |             0     |
| gemini     | L1      | en         | state_sp    |         5 |             2 |    0.4837 |                 0.4837 |            -0.2871 |        0      |             0     |
| gemini     | L1      | pt-BR      | brazil      |         5 |             4 |  175.451  |                21.5959 |             1.354  |        1.5416 |             0     |
| gemini     | L1      | pt-BR      | global      |         5 |             5 |  351.484  |                35.399  |             1.5611 |        1.781  |             0     |
| gemini     | L1      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gemini     | L2      | en         | brazil      |         5 |             5 |    0.4413 |                 0.4549 |            -0.2635 |        0.3761 |             0.2   |
| gemini     | L2      | en         | global      |         5 |             5 |    0.7507 |                 0.3778 |             0.1392 |        0.3315 |             0.2   |
| gemini     | L2      | en         | state_sp    |         5 |             2 |    0.9306 |                 0.9306 |            -1.159  |        0      |             0     |
| gemini     | L2      | pt-BR      | brazil      |         5 |             5 |    1.3405 |                 0.6946 |            -0.5152 |        1.5287 |             0     |
| gemini     | L2      | pt-BR      | global      |         5 |             5 |    3.8551 |                 0.5649 |             0.1945 |        1.3685 |             0     |
| gemini     | L2      | pt-BR      | state_sp    |         5 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gemini     | L3      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |             1     |
| gemini     | L3      | en         | global      |         5 |             5 |    0      |                 0.0001 |             0      |        0      |             1     |
| gemini     | L3      | en         | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |             1     |
| gemini     | L3      | pt-BR      | brazil      |        20 |            20 |    0.0359 |                 0.0008 |            -0.0003 |        0.1589 |             0.95  |
| gemini     | L3      | pt-BR      | global      |        20 |            20 |    0.0314 |                 0.0001 |             0      |        0.1411 |             0.95  |
| gemini     | L3      | pt-BR      | state_sp    |        20 |            20 |    0.0357 |                 0.0002 |             0.0001 |        0.1609 |             0.95  |
| gemini     | L4      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |             1     |
| gemini     | L4      | en         | global      |         5 |             5 |    0      |                 0      |             0      |        0      |             1     |
| gemini     | L4      | en         | state_sp    |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |             1     |
| gemini     | L4      | pt-BR      | brazil      |        20 |            20 |    0.0008 |                 0.0008 |            -0.0003 |        0      |             1     |
| gemini     | L4      | pt-BR      | global      |        20 |            20 |    0      |                 0      |             0      |        0      |             1     |
| gemini     | L4      | pt-BR      | state_sp    |        20 |            20 |    0.0002 |                 0.0002 |             0.0001 |        0      |             1     |
| gpt        | L0      | en         | brazil      |        10 |            10 |    1.7628 |                 2.4535 |             0.5383 |        0.3288 |             0     |
| gpt        | L0      | en         | global      |        10 |            10 |    5.9971 |                 7.8347 |             0.9462 |        0.3217 |             0     |
| gpt        | L0      | en         | state_sp    |        10 |             1 |    0.8274 |                 0.8274 |            -0.7629 |        0      |             0     |
| gpt        | L0      | pt-BR      | brazil      |        10 |            10 |    0.7761 |                 0.4801 |             0.1703 |        0.2546 |             0     |
| gpt        | L0      | pt-BR      | global      |        10 |            10 |    5.7144 |                 6.0678 |             0.8493 |        0.1579 |             0     |
| gpt        | L0      | pt-BR      | state_sp    |        10 |             3 |    0.6548 |                 0.6548 |            -0.4619 |        0      |             0     |
| gpt        | L1      | en         | brazil      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L1      | en         | global      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L1      | en         | state_sp    |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L1      | pt-BR      | brazil      |        10 |            10 |    1.7628 |                 1.2201 |             0.3464 |        0.2739 |             0     |
| gpt        | L1      | pt-BR      | global      |        10 |            10 |    7.3753 |                 7.8347 |             0.9462 |        0.1646 |             0     |
| gpt        | L1      | pt-BR      | state_sp    |        10 |             3 |    0.8117 |                 0.8117 |            -0.7251 |        0      |             0     |
| gpt        | L2      | en         | brazil      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L2      | en         | global      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L2      | en         | state_sp    |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L2      | pt-BR      | brazil      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L2      | pt-BR      | global      |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L2      | pt-BR      | state_sp    |        10 |             0 |  nan      |               nan      |           nan      |      nan      |             0     |
| gpt        | L3      | en         | brazil      |        10 |            10 |    0.2028 |                 0.2164 |            -0.0619 |        0.212  |             1     |
| gpt        | L3      | en         | global      |        10 |            10 |    0.1594 |                 0.1398 |            -0.0287 |        0.173  |             1     |
| gpt        | L3      | en         | state_sp    |        10 |             5 |    0.2296 |                 0.2317 |             0.0905 |        0.2106 |             0.5   |
| gpt        | L3      | pt-BR      | brazil      |        25 |            25 |    0.5395 |                 0.2472 |             0.0851 |        0.6532 |             0.6   |
| gpt        | L3      | pt-BR      | global      |        25 |            25 |    0.1642 |                 0.0862 |             0.0359 |        0.2704 |             0.84  |
| gpt        | L3      | pt-BR      | state_sp    |        25 |            20 |    0.257  |                 0.2533 |             0.0646 |        0.2649 |             0.6   |
| gpt        | L4      | en         | brazil      |         8 |             8 |    0.4444 |                 0.141  |             0.0118 |        0.3978 |             0.625 |
| gpt        | L4      | en         | global      |         8 |             8 |    0.2888 |                 0.1061 |            -0.0487 |        0.3688 |             0.625 |
| gpt        | L4      | en         | state_sp    |         8 |             5 |    0.0686 |                 0.0537 |             0.0001 |        0.0819 |             0.625 |
| gpt        | L4      | pt-BR      | brazil      |        25 |            25 |    0.365  |                 0.141  |            -0.006  |        0.5531 |             0.68  |
| gpt        | L4      | pt-BR      | global      |        25 |            25 |    0.1621 |                 0.0366 |            -0.0162 |        0.277  |             0.8   |
| gpt        | L4      | pt-BR      | state_sp    |        25 |            20 |    0.1675 |                 0.1295 |             0.0001 |        0.2127 |             0.68  |