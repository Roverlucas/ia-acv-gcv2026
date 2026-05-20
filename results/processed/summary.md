# Aggregated results


## MAPE by (LLM × level × language)


|                       |       en |    pt-BR |
|:----------------------|---------:|---------:|
| (1, 'deepseek', 'L0') |   20.244 |    2.125 |
| (1, 'deepseek', 'L1') |   20.244 |   89.425 |
| (1, 'deepseek', 'L2') | 2017.92  |    2.158 |
| (1, 'deepseek', 'L3') |    0.149 |   17.623 |
| (1, 'deepseek', 'L4') |    0.046 |    0.197 |
| (1, 'gemini', 'L0')   |   16.864 |    5.782 |
| (1, 'gemini', 'L1')   |  110.041 |  273.247 |
| (1, 'gemini', 'L2')   |    0.652 |    2.598 |
| (1, 'gemini', 'L3')   |    0     |    0.034 |
| (1, 'gemini', 'L4')   |    0     |    0     |
| (1, 'gpt', 'L0')      |    2.453 |    2.489 |
| (1, 'gpt', 'L1')      |  nan     |    3.936 |
| (1, 'gpt', 'L2')      |  nan     |  nan     |
| (1, 'gpt', 'L3')      |    0.174 |    0.189 |
| (1, 'gpt', 'L4')      |    0.075 |    0.124 |
| (2, 'deepseek', 'L0') |   48.853 |    4.229 |
| (2, 'deepseek', 'L1') |   49.477 |   38.434 |
| (2, 'deepseek', 'L2') | 4306.15  | 2995.78  |
| (2, 'deepseek', 'L3') |    0.441 | 1242.14  |
| (2, 'deepseek', 'L4') |    0.358 |    0.484 |
| (2, 'gemini', 'L0')   |   62.077 |   51.206 |
| (2, 'gemini', 'L1')   |  702.492 |  898.552 |
| (2, 'gemini', 'L2')   |    2.308 |    1.376 |
| (2, 'gemini', 'L3')   |    0     |    0     |
| (2, 'gemini', 'L4')   |    0     |    0     |
| (2, 'gpt', 'L0')      |   10.035 |    7.744 |
| (2, 'gpt', 'L1')      |  nan     |    8.71  |
| (2, 'gpt', 'L2')      |  nan     |  nan     |
| (2, 'gpt', 'L3')      |    0.41  |    1.406 |
| (2, 'gpt', 'L4')      |    0.355 |    0.5   |


## Aggregated table


|   system | provider   | level   | language   | geo_scope   |   n_total |   n_responded |      mape |   median_abs_rel_error |   median_log_ratio |   cv_estimate |   share_within_30 |
|---------:|:-----------|:--------|:-----------|:------------|----------:|--------------:|----------:|-----------------------:|-------------------:|--------------:|------------------:|
|        1 | deepseek   | L0      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |              0    |
|        1 | deepseek   | L0      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |              0    |
|        1 | deepseek   | L0      | en         | state       |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |              0    |
|        1 | deepseek   | L0      | pt-BR      | brazil      |         5 |             5 |    1.4668 |                 1.4668 |             0.3921 |        0      |              0    |
|        1 | deepseek   | L0      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |              0    |
|        1 | deepseek   | L0      | pt-BR      | state       |         5 |             5 |    0.6077 |                 0.6077 |            -0.4064 |        0      |              0    |
|        1 | deepseek   | L1      | en         | brazil      |         5 |             5 |   17.501  |                17.501  |             1.2672 |        0      |              0    |
|        1 | deepseek   | L1      | en         | global      |         5 |             5 |   41.4066 |                41.4066 |             1.6274 |        0      |              0    |
|        1 | deepseek   | L1      | en         | state       |         5 |             5 |    1.8245 |                 1.8245 |             0.4509 |        0      |              0    |
|        1 | deepseek   | L1      | pt-BR      | brazil      |         5 |             5 |   77.4938 |                17.501  |             1.2672 |        1.1107 |              0    |
|        1 | deepseek   | L1      | pt-BR      | global      |         5 |             5 |  179.228  |                41.4066 |             1.6274 |        1.1072 |              0    |
|        1 | deepseek   | L1      | pt-BR      | state       |         5 |             5 |   11.5532 |                 1.8245 |             0.4509 |        1.1124 |              0    |
|        1 | deepseek   | L2      | en         | brazil      |         5 |             4 | 1516.09   |              1516.09   |             3.181  |        0      |              0    |
|        1 | deepseek   | L2      | en         | global      |         5 |             4 | 4345.68   |              4345.68   |             3.6382 |        0      |              0    |
|        1 | deepseek   | L2      | en         | state       |         5 |             4 |  192.01   |               192.01   |             2.2856 |        0      |              0    |
|        1 | deepseek   | L2      | pt-BR      | brazil      |         5 |             5 |    0.8501 |                 0.8501 |             0.2672 |        0      |              0    |
|        1 | deepseek   | L2      | pt-BR      | global      |         5 |             5 |    4.3008 |                 4.3008 |             0.7243 |        0      |              0    |
|        1 | deepseek   | L2      | pt-BR      | state       |         5 |             3 |    0.7646 |                 0.7646 |            -0.6282 |        0      |              0    |
|        1 | deepseek   | L3      | en         | brazil      |         5 |             5 |    0.0715 |                 0.0953 |             0.0395 |        0.0348 |              1    |
|        1 | deepseek   | L3      | en         | global      |         5 |             5 |    0.3499 |                 0.3499 |             0.1303 |        0      |              0    |
|        1 | deepseek   | L3      | en         | state       |         5 |             5 |    0.0258 |                 0.0294 |             0.0032 |        0.0276 |              1    |
|        1 | deepseek   | L3      | pt-BR      | brazil      |        20 |            19 |   16.3749 |                 0.2193 |             0.0859 |        3.9698 |              0.65 |
|        1 | deepseek   | L3      | pt-BR      | global      |        20 |            19 |   20.6738 |                 0.3499 |             0.1303 |        4.0144 |              0.45 |
|        1 | deepseek   | L3      | pt-BR      | state       |        20 |            19 |   15.8196 |                 0.2264 |             0.0742 |        3.968  |              0.75 |
|        1 | deepseek   | L4      | en         | brazil      |         5 |             5 |    0.0442 |                 0.0527 |            -0.0235 |        0.0321 |              1    |
|        1 | deepseek   | L4      | en         | global      |         5 |             5 |    0.0178 |                 0.0178 |             0.0076 |        0      |              1    |
|        1 | deepseek   | L4      | en         | state       |         5 |             5 |    0.0754 |                 0.0867 |            -0.0394 |        0.0244 |              1    |
|        1 | deepseek   | L4      | pt-BR      | brazil      |        20 |            19 |    0.1887 |                 0.0527 |            -0.0235 |        0.4611 |              0.9  |
|        1 | deepseek   | L4      | pt-BR      | global      |        20 |            19 |    0.1882 |                 0.0211 |            -0.0093 |        0.5589 |              0.85 |
|        1 | deepseek   | L4      | pt-BR      | state       |        20 |            19 |    0.2135 |                 0.0867 |            -0.0394 |        0.4544 |              0.9  |
|        1 | gemini     | L0      | en         | brazil      |         5 |             5 |   14.8887 |                10.261  |             1.0516 |        0.5521 |              0    |
|        1 | gemini     | L0      | en         | global      |         5 |             5 |   33.5331 |                25.0801 |             1.4163 |        0.5154 |              0    |
|        1 | gemini     | L0      | en         | state       |         5 |             5 |    2.1691 |                 2.3722 |             0.5279 |        0.1589 |              0    |
|        1 | gemini     | L0      | pt-BR      | brazil      |         5 |             5 |    3.2427 |                 0.1367 |            -0.0639 |        1.6273 |              0.6  |
|        1 | gemini     | L0      | pt-BR      | global      |         5 |             5 |    8.3215 |                 2.5339 |             0.5483 |        1.3806 |              0.2  |
|        1 | gemini     | L0      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gemini     | L1      | en         | brazil      |         5 |             5 |   80.9769 |                22.6813 |             1.3744 |        1.0951 |              0    |
|        1 | gemini     | L1      | en         | global      |         5 |             5 |  182.929  |                91.5878 |             1.9666 |        1.0177 |              0    |
|        1 | gemini     | L1      | en         | state       |         5 |             2 |    0.4837 |                 0.4837 |            -0.2871 |        0      |              0    |
|        1 | gemini     | L1      | pt-BR      | brazil      |         5 |             4 |  175.451  |                21.5959 |             1.354  |        1.5416 |              0    |
|        1 | gemini     | L1      | pt-BR      | global      |         5 |             5 |  351.484  |                35.399  |             1.5611 |        1.781  |              0    |
|        1 | gemini     | L1      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gemini     | L2      | en         | brazil      |         5 |             5 |    0.4413 |                 0.4549 |            -0.2635 |        0.3761 |              0.2  |
|        1 | gemini     | L2      | en         | global      |         5 |             5 |    0.7507 |                 0.3778 |             0.1392 |        0.3315 |              0.2  |
|        1 | gemini     | L2      | en         | state       |         5 |             2 |    0.9306 |                 0.9306 |            -1.159  |        0      |              0    |
|        1 | gemini     | L2      | pt-BR      | brazil      |         5 |             5 |    1.3405 |                 0.6946 |            -0.5152 |        1.5287 |              0    |
|        1 | gemini     | L2      | pt-BR      | global      |         5 |             5 |    3.8551 |                 0.5649 |             0.1945 |        1.3685 |              0    |
|        1 | gemini     | L2      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gemini     | L3      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |              1    |
|        1 | gemini     | L3      | en         | global      |         5 |             5 |    0      |                 0.0001 |             0      |        0      |              1    |
|        1 | gemini     | L3      | en         | state       |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |              1    |
|        1 | gemini     | L3      | pt-BR      | brazil      |        20 |            20 |    0.0359 |                 0.0008 |            -0.0003 |        0.1589 |              0.95 |
|        1 | gemini     | L3      | pt-BR      | global      |        20 |            20 |    0.0314 |                 0.0001 |             0      |        0.1411 |              0.95 |
|        1 | gemini     | L3      | pt-BR      | state       |        20 |            20 |    0.0357 |                 0.0002 |             0.0001 |        0.1609 |              0.95 |
|        1 | gemini     | L4      | en         | brazil      |         5 |             5 |    0.0008 |                 0.0008 |            -0.0003 |        0      |              1    |
|        1 | gemini     | L4      | en         | global      |         5 |             5 |    0      |                 0      |             0      |        0      |              1    |
|        1 | gemini     | L4      | en         | state       |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0      |              1    |
|        1 | gemini     | L4      | pt-BR      | brazil      |        20 |            20 |    0.0008 |                 0.0008 |            -0.0003 |        0      |              1    |
|        1 | gemini     | L4      | pt-BR      | global      |        20 |            20 |    0      |                 0      |             0      |        0      |              1    |
|        1 | gemini     | L4      | pt-BR      | state       |        20 |            20 |    0.0002 |                 0.0002 |             0.0001 |        0      |              1    |
|        1 | gpt        | L0      | en         | brazil      |         5 |             5 |    1.0721 |                 0.8501 |             0.2672 |        0.4027 |              0    |
|        1 | gpt        | L0      | en         | global      |         5 |             5 |    4.1595 |                 3.2407 |             0.6274 |        0.3562 |              0    |
|        1 | gpt        | L0      | en         | state       |         5 |             1 |    0.8274 |                 0.8274 |            -0.7629 |        0      |              0    |
|        1 | gpt        | L0      | pt-BR      | brazil      |         5 |             5 |    1.0721 |                 1.4668 |             0.3921 |        0.2333 |              0    |
|        1 | gpt        | L0      | pt-BR      | global      |         5 |             5 |    5.0076 |                 4.3008 |             0.7243 |        0.1441 |              0    |
|        1 | gpt        | L0      | pt-BR      | state       |         5 |             3 |    0.6548 |                 0.6548 |            -0.4619 |        0      |              0    |
|        1 | gpt        | L1      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L1      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L1      | en         | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L1      | pt-BR      | brazil      |         5 |             5 |    1.9108 |                 1.2201 |             0.3464 |        0.2906 |              0    |
|        1 | gpt        | L1      | pt-BR      | global      |         5 |             5 |    7.8347 |                 7.8347 |             0.9462 |        0      |              0    |
|        1 | gpt        | L1      | pt-BR      | state       |         5 |             3 |    0.8117 |                 0.8117 |            -0.7251 |        0      |              0    |
|        1 | gpt        | L2      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L2      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L2      | en         | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L2      | pt-BR      | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L2      | pt-BR      | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L2      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        1 | gpt        | L3      | en         | brazil      |         5 |             5 |    0.2072 |                 0.2164 |             0.0851 |        0.1877 |              1    |
|        1 | gpt        | L3      | en         | global      |         5 |             5 |    0.0862 |                 0.0862 |             0.0359 |        0      |              1    |
|        1 | gpt        | L3      | en         | state       |         5 |             5 |    0.2296 |                 0.2317 |             0.0905 |        0.2106 |              1    |
|        1 | gpt        | L3      | pt-BR      | brazil      |        20 |            20 |    0.2389 |                 0.2472 |             0.0592 |        0.2461 |              0.75 |
|        1 | gpt        | L3      | pt-BR      | global      |        20 |            20 |    0.0698 |                 0.0862 |             0.0359 |        0.0401 |              1    |
|        1 | gpt        | L3      | pt-BR      | state       |        20 |            20 |    0.257  |                 0.2533 |             0.0646 |        0.2649 |              0.75 |
|        1 | gpt        | L4      | en         | brazil      |         5 |             5 |    0.0702 |                 0.0398 |            -0.006  |        0.0817 |              1    |
|        1 | gpt        | L4      | en         | global      |         5 |             5 |    0.086  |                 0.0727 |            -0.0328 |        0.0197 |              1    |
|        1 | gpt        | L4      | en         | state       |         5 |             5 |    0.0686 |                 0.0537 |             0.0001 |        0.0819 |              1    |
|        1 | gpt        | L4      | pt-BR      | brazil      |        20 |            20 |    0.157  |                 0.1319 |            -0.006  |        0.1946 |              0.85 |
|        1 | gpt        | L4      | pt-BR      | global      |        20 |            20 |    0.0475 |                 0.0364 |            -0.0161 |        0.0385 |              1    |
|        1 | gpt        | L4      | pt-BR      | state       |        20 |            20 |    0.1675 |                 0.1295 |             0.0001 |        0.2127 |              0.85 |
|        2 | deepseek   | L0      | en         | brazil      |         5 |             5 |   12.691  |                12.691  |             1.1364 |        0      |              0    |
|        2 | deepseek   | L0      | en         | global      |         5 |             5 |   92.6676 |                92.6676 |             1.9716 |        0      |              0    |
|        2 | deepseek   | L0      | en         | state       |         5 |             1 |   10.5856 |                10.5856 |             1.0639 |        0      |              0    |
|        2 | deepseek   | L0      | pt-BR      | brazil      |         5 |             5 |    0.8255 |                 0.8255 |             0.2614 |        0      |              0    |
|        2 | deepseek   | L0      | pt-BR      | global      |         5 |             5 |   10.7084 |                10.7084 |             1.0685 |        0      |              0    |
|        2 | deepseek   | L0      | pt-BR      | state       |         5 |             4 |    0.3838 |                 0.3838 |             0.1353 |        0.1628 |              0.4  |
|        2 | deepseek   | L1      | en         | brazil      |         5 |             5 |   17.2546 |                17.2546 |             1.2614 |        0      |              0    |
|        2 | deepseek   | L1      | en         | global      |         5 |             5 |  116.085  |               116.085  |             2.0685 |        0      |              0    |
|        2 | deepseek   | L1      | en         | state       |         5 |             5 |   15.0912 |                15.0912 |             1.2066 |        0      |              0    |
|        2 | deepseek   | L1      | pt-BR      | brazil      |         5 |             5 |   12.691  |                12.691  |             1.1364 |        0      |              0    |
|        2 | deepseek   | L1      | pt-BR      | global      |         5 |             5 |   92.6676 |                92.6676 |             1.9716 |        0      |              0    |
|        2 | deepseek   | L1      | pt-BR      | state       |         5 |             5 |    9.942  |                10.5856 |             1.0639 |        0.1176 |              0    |
|        2 | deepseek   | L2      | en         | brazil      |         5 |             5 | 1121.66   |              1121.66   |             3.0502 |        0      |              0    |
|        2 | deepseek   | L2      | en         | global      |         5 |             5 | 9599.93   |              9599.93   |             3.9823 |        0      |              0    |
|        2 | deepseek   | L2      | en         | state       |         5 |             3 |  790.685  |               790.685  |             2.8986 |        0      |              0    |
|        2 | deepseek   | L2      | pt-BR      | brazil      |         5 |             5 |  875.495  |              1094.28   |             3.0395 |        0.4992 |              0    |
|        2 | deepseek   | L2      | pt-BR      | global      |         5 |             5 | 7494.75   |              9365.76   |             3.9716 |        0.4992 |              0    |
|        2 | deepseek   | L2      | pt-BR      | state       |         5 |             5 |  617.107  |               771.376  |             2.8878 |        0.4992 |              0.2  |
|        2 | deepseek   | L3      | en         | brazil      |         5 |             4 |    0.2002 |                 0.2002 |             0.0792 |        0.0114 |              0.8  |
|        2 | deepseek   | L3      | en         | global      |         5 |             4 |    0.6236 |                 0.6236 |             0.2105 |        0      |              0    |
|        2 | deepseek   | L3      | en         | state       |         5 |             4 |    0.4997 |                 0.4997 |             0.176  |        0      |              0    |
|        2 | deepseek   | L3      | pt-BR      | brazil      |         5 |             5 | 1167.3    |              1185.55   |             3.0743 |        0.0312 |              0    |
|        2 | deepseek   | L3      | pt-BR      | global      |         5 |             5 | 1169.85   |              1169.85   |             3.0685 |        0      |              0    |
|        2 | deepseek   | L3      | pt-BR      | state       |         5 |             5 | 1389.28   |              1415.02   |             3.1511 |        0.037  |              0    |
|        2 | deepseek   | L4      | en         | brazil      |         5 |             4 |    0.1688 |                 0.1829 |             0.0729 |        0.0276 |              0.8  |
|        2 | deepseek   | L4      | en         | global      |         5 |             4 |    0.3839 |                 0.3839 |             0.141  |        0.0265 |              0    |
|        2 | deepseek   | L4      | en         | state       |         5 |             4 |    0.5225 |                 0.5467 |             0.1892 |        0.0518 |              0    |
|        2 | deepseek   | L4      | pt-BR      | brazil      |         5 |             5 |    0.2523 |                 0.2504 |             0.0971 |        0.0208 |              1    |
|        2 | deepseek   | L4      | pt-BR      | global      |         5 |             5 |    0.6704 |                 0.6704 |             0.2228 |        0      |              0    |
|        2 | deepseek   | L4      | pt-BR      | state       |         5 |             5 |    0.5293 |                 0.4997 |             0.176  |        0.0387 |              0    |
|        2 | gemini     | L0      | en         | brazil      |         5 |             5 |   15.4532 |                14.7902 |             1.1984 |        0.5497 |              0    |
|        2 | gemini     | L0      | en         | global      |         5 |             5 |  128.535  |               157.376  |             2.1997 |        0.3974 |              0    |
|        2 | gemini     | L0      | en         | state       |         5 |             2 |   12.4926 |                12.4926 |             0.8215 |        0.871  |              0    |
|        2 | gemini     | L0      | pt-BR      | brazil      |         5 |             5 |   10.4822 |                10.2266 |             1.0502 |        0.5035 |              0    |
|        2 | gemini     | L0      | pt-BR      | global      |         5 |             5 |   91.9307 |                95.0093 |             1.9823 |        0.4632 |              0    |
|        2 | gemini     | L0      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gemini     | L1      | en         | brazil      |         5 |             5 |  213.272  |                16.3419 |             1.2391 |        1.8769 |              0    |
|        2 | gemini     | L1      | en         | global      |         5 |             5 | 1330.34   |               109.059  |             2.0416 |        1.8636 |              0    |
|        2 | gemini     | L1      | en         | state       |         5 |             1 |    9.3627 |                 9.3627 |             1.0155 |        0      |              0    |
|        2 | gemini     | L1      | pt-BR      | brazil      |         5 |             4 |    7.9423 |                 8.1045 |             0.733  |        0.8516 |              0.2  |
|        2 | gemini     | L1      | pt-BR      | global      |         5 |             5 | 1611.04   |               116.085  |             2.0685 |        1.9237 |              0    |
|        2 | gemini     | L1      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gemini     | L2      | en         | brazil      |         5 |             3 |    0.7511 |                 0.7105 |            -0.5311 |        0.9696 |              0    |
|        2 | gemini     | L2      | en         | global      |         5 |             5 |    3.6633 |                 1.2519 |             0.3526 |        0.8873 |              0    |
|        2 | gemini     | L2      | en         | state       |         5 |             1 |    0.2062 |                 0.2062 |             0.0814 |        0      |              0.2  |
|        2 | gemini     | L2      | pt-BR      | brazil      |         5 |             1 |    0.5136 |                 0.5136 |            -0.313  |        0      |              0    |
|        2 | gemini     | L2      | pt-BR      | global      |         5 |             5 |    1.5481 |                 1.5376 |             0.4044 |        0.2714 |              0    |
|        2 | gemini     | L2      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gemini     | L3      | en         | brazil      |         5 |             5 |    0.0003 |                 0.0004 |             0.0002 |        0.0001 |              1    |
|        2 | gemini     | L3      | en         | global      |         5 |             5 |    0.0001 |                 0.0001 |            -0      |        0.0001 |              1    |
|        2 | gemini     | L3      | en         | state       |         5 |             5 |    0.0002 |                 0.0002 |             0.0001 |        0.0001 |              1    |
|        2 | gemini     | L3      | pt-BR      | brazil      |         5 |             5 |    0.0002 |                 0      |            -0      |        0.0002 |              1    |
|        2 | gemini     | L3      | pt-BR      | global      |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0.0001 |              1    |
|        2 | gemini     | L3      | pt-BR      | state       |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0.0001 |              1    |
|        2 | gemini     | L4      | en         | brazil      |         5 |             5 |    0      |                 0      |            -0      |        0      |              1    |
|        2 | gemini     | L4      | en         | global      |         5 |             5 |    0      |                 0      |             0      |        0      |              1    |
|        2 | gemini     | L4      | en         | state       |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0      |              1    |
|        2 | gemini     | L4      | pt-BR      | brazil      |         5 |             5 |    0      |                 0      |            -0      |        0      |              1    |
|        2 | gemini     | L4      | pt-BR      | global      |         5 |             5 |    0      |                 0      |             0      |        0      |              1    |
|        2 | gemini     | L4      | pt-BR      | state       |         5 |             5 |    0.0001 |                 0.0001 |             0      |        0      |              1    |
|        2 | gpt        | L0      | en         | brazil      |         5 |             5 |    1.5556 |                 1.5556 |             0.4075 |        0      |              0    |
|        2 | gpt        | L0      | en         | global      |         5 |             5 |   18.5141 |                18.5141 |             1.2903 |        0      |              0    |
|        2 | gpt        | L0      | en         | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L0      | pt-BR      | brazil      |         5 |             5 |    0.0953 |                 0.0953 |             0.0395 |        0      |              1    |
|        2 | gpt        | L0      | pt-BR      | global      |         5 |             5 |   15.3918 |                14.6113 |             1.1934 |        0.0952 |              0    |
|        2 | gpt        | L0      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L1      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L1      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L1      | en         | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L1      | pt-BR      | brazil      |         5 |             5 |    0.935  |                 0.6429 |             0.2156 |        0.2375 |              0    |
|        2 | gpt        | L1      | pt-BR      | global      |         5 |             5 |   16.4846 |                18.5141 |             1.2903 |        0.2321 |              0    |
|        2 | gpt        | L1      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | en         | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | en         | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | en         | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | pt-BR      | brazil      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | pt-BR      | global      |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L2      | pt-BR      | state       |         5 |             0 |  nan      |               nan      |           nan      |      nan      |              0    |
|        2 | gpt        | L3      | en         | brazil      |         5 |             5 |    0.4068 |                 0.4433 |            -0.2544 |        0.0754 |              0    |
|        2 | gpt        | L3      | en         | global      |         5 |             5 |    0.695  |                 0.7076 |             0.2324 |        0.0314 |              0    |
|        2 | gpt        | L3      | en         | state       |         5 |             5 |    0.1282 |                 0.0596 |             0.0251 |        0.0955 |              1    |
|        2 | gpt        | L3      | pt-BR      | brazil      |        10 |            10 |    2.0675 |                 2.7091 |             0.5693 |        0.4027 |              0    |
|        2 | gpt        | L3      | pt-BR      | global      |        10 |            10 |    0.4938 |                 0.6187 |             0.2092 |        0.3177 |              0.4  |
|        2 | gpt        | L3      | pt-BR      | state       |        10 |            10 |    1.6578 |                 2.2259 |             0.5087 |        0.4022 |              0    |
|        2 | gpt        | L4      | en         | brazil      |         5 |             5 |    0.5491 |                 0.5772 |             0.1979 |        0.0276 |              0    |
|        2 | gpt        | L4      | en         | global      |         5 |             5 |    0.1701 |                 0.1617 |            -0.0766 |        0.0203 |              1    |
|        2 | gpt        | L4      | en         | state       |         5 |             5 |    0.3466 |                 0.3672 |             0.1358 |        0.0212 |              0.2  |
|        2 | gpt        | L4      | pt-BR      | brazil      |        10 |            10 |    0.7613 |                 0.8306 |             0.2319 |        0.5384 |              0    |
|        2 | gpt        | L4      | pt-BR      | global      |        10 |            10 |    0.2035 |                 0.1619 |            -0.0767 |        0.2434 |              0.9  |
|        2 | gpt        | L4      | pt-BR      | state       |        10 |            10 |    0.5357 |                 0.6022 |             0.1699 |        0.4202 |              0    |