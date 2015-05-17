NOTE: This wiki page is now obsolete. See http://mpmath.googlecode.com/svn/bench/mpbench.html for up to date benchmarks.

## Basic operations ##

The time needed to perform some basic calculations at precision levels between 10 and 10,000 decimal digits are given in the following table. The times were measured on an Athlon 3700+ (2.21 GHz), using Python 2.5.1 and with [Psyco](http://psyco.sourceforge.net/) enabled. All times are in milliseconds (ranging from 1/500,000 of a second for a low-precision addition to 4.6 seconds for a 10,000-digit sine).

The inputs are x = sqrt(3) and y = sqrt(5).

| **op/dps** | **10** | **100** | **1000** | **10,000** |
|:-----------|:-------|:--------|:---------|:-----------|
|add(x,y)    | 0.0022 ms | 0.0021 ms | 0.0049 ms | 0.0036 ms  |
|mul(x,y)    | 0.0025 ms | 0.0041 ms |  0.12 ms  |   5.0 ms   |
|div(x,y)    | 0.0040 ms | 0.011 ms  |  0.41 ms  |   37 ms    |
|sqrt(x)     | 0.0096 ms | 0.020 ms  |  0.32 ms  |   25 ms    |
| exp(x)     |  0.012 ms | 0.069 ms  |  8.0 ms   |  1200 ms   |
| log(x)     |  0.030 ms |  0.13 ms  |  8.7 ms   |  1200 ms   |
| sin(x)     |  0.026 ms |  0.10 ms  |   15 ms   |  4600 ms   |

For comparison, timings for the same operations for several other arbitrary-precision libraries are [listed on the PARI website](http://pari.math.u-bordeaux.fr/benchs/timings-mpfr.html). Mpmath stands up fairly well considering that it is written in an interpreted language: although generally at least an order of magnitude slower than the fastest library (MPFR), it is comparable in speed to Maple, ArPrec and MuPAD.

In the author's experience, mpmath is typically 2-10 times slower than Mathematica 5 for high-precision numerical integration and similar high-level tasks (but actually faster on rare occasions).

## Detailed benchmarks vs Decimal ##

The following benchmarks measure the number of operations that can be carried out per second at the given precision with x and y being random full-precision numbers between 0 and 32. "Decimal" means that the `decimal.Decimal` class is used, "mpf" means that the `mpmath.mpf` class is used, and "raw mpf" means that the operations are performed using the low-level functions in `mpmath.lib` (this avoids the overhead of creating mpf instances). The three rightmost columns list the same benchmark but with Psyco enabled.

Numbers in parentheses indicate the speedup compared to Decimals. In summary, mpmath operations are generally around 2-10 times faster at low to medium precision and nearly all operations are much faster asymptotically. (The obvious exception is conversion to strings, where Decimals don't need to do any work.)

(The tests for powers, exp and log only go up to 1000 digits as the decimal versions took too long to finish at 3000 digits.)

**Convert to integer (int(x))**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 350000      | 410000 (1.2x) | 840000 (2.4x) | 510000            | 550000 (1.1x) | 3470000 (6.7x)    |
| 30         | 350000      | 420000 (1.2x) | 870000 (2.5x) | 510000            | 650000 (1.3x) | 4970000 (9.6x)    |
| 100        | 350000      | 420000 (1.2x) | 860000 (2.5x) | 510000            | 620000 (1.2x) | 4640000 (9.0x)    |
| 300        | 350000      | 420000 (1.2x) | 860000 (2.5x) | 510000            | 640000 (1.3x) | 4700000 (9.2x)    |
| 1000       | 350000      | 420000 (1.2x) | 850000 (2.4x) | 510000            | 630000 (1.2x) | 4770000 (9.2x)    |
| 3000       | 350000      | 420000 (1.2x) | 870000 (2.5x) | 520000            | 650000 (1.2x) | 4640000 (8.8x)    |

**Convert to string (str(x))**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 250000      | 41000 (0.2x) | 42000 (0.2x) | 450000            | 60000 (0.1x)  | 57000 (0.1x)      |
| 30         | 240000      | 36000 (0.1x) | 36000 (0.1x) | 440000            | 50000 (0.1x)  | 50000 (0.1x)      |
| 100        | 240000      | 14000 (0.1x) | 14000 (0.1x) | 450000            | 16000 (0.0x)  | 16000 (0.0x)      |
| 300        | 210000      | 3200 (0.0x) | 3400 (0.0x)  | 350000            | 3300 (0.0x)   | 3500 (0.0x)       |
| 1000       | 180000      | 430 (0.0x) | 430 (0.0x)   | 280000            | 430 (0.0x)    | 430 (0.0x)        |
| 3000       | 150000      | 44 (0.0x) | 50 (0.0x)    | 200000            | 45 (0.0x)     | 50 (0.0x)         |

**Convert to float (float(x))**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 120000      | 310000 (2.5x) | 530000 (4.2x) | 150000            | 420000 (2.8x) | 1220000 (8.0x)    |
| 30         | 110000      | 250000 (2.3x) | 390000 (3.5x) | 130000            | 370000 (2.8x) | 900000 (6.9x)     |
| 100        | 97000       | 250000 (2.6x) | 390000 (4.0x) | 110000            | 370000 (3.4x) | 900000 (8.2x)     |
| 300        | 56000       | 250000 (4.5x) | 390000 (7.0x) | 75000             | 370000 (5.0x) | 910000 (12.2x)    |
| 1000       | 26000       | 250000 (9.6x) | 390000 (14.9x) | 35000             | 370000 (10.3x) | 890000 (24.9x)    |
| 3000       | 10000       | 250000 (24.4x) | 390000 (37.5x) | 14000             | 370000 (25.7x) | 920000 (62.7x)    |

**Equality (x==y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 130000      | 520000 (4.1x) | 1300000 (10.0x) | 290000            | 700000 (2.4x) | 5260000 (18.0x)   |
| 30         | 130000      | 520000 (3.9x) | 1230000 (9.3x) | 310000            | 700000 (2.2x) | 6270000 (19.7x)   |
| 100        | 120000      | 510000 (4.0x) | 1230000 (9.5x) | 310000            | 700000 (2.2x) | 6270000 (19.9x)   |
| 300        | 130000      | 510000 (3.9x) | 1230000 (9.4x) | 290000            | 700000 (2.4x) | 5420000 (18.2x)   |
| 1000       | 130000      | 500000 (3.9x) | 1160000 (9.0x) | 290000            | 710000 (2.4x) | 6390000 (21.7x)   |
| 3000       | 120000      | 500000 (3.9x) | 1310000 (10.2x) | 280000            | 710000 (2.5x) | 5340000 (18.6x)   |

**Comparison (x<y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 130000      | 280000 (2.0x) | 780000 (5.6x) | 280000            | 650000 (2.3x) | 13760000 (48.2x)  |
| 30         | 130000      | 280000 (2.0x) | 770000 (5.6x) | 290000            | 650000 (2.2x) | 14910000 (50.2x)  |
| 100        | 130000      | 280000 (2.0x) | 770000 (5.6x) | 290000            | 620000 (2.2x) | 14910000 (51.4x)  |
| 300        | 140000      | 280000 (2.0x) | 770000 (5.5x) | 280000            | 620000 (2.2x) | 14310000 (50.0x)  |
| 1000       | 140000      | 280000 (2.0x) | 770000 (5.5x) | 280000            | 630000 (2.3x) | 14310000 (50.6x)  |
| 3000       | 140000      | 280000 (2.0x) | 770000 (5.4x) | 270000            | 670000 (2.5x) | 14310000 (52.5x)  |

**Addition (x+y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 19000       | 120000 (6.5x) | 160000 (8.5x) | 40000             | 270000 (6.7x) | 590000 (14.6x)    |
| 30         | 18000       | 110000 (6.3x) | 140000 (8.0x) | 36000             | 240000 (6.8x) | 480000 (13.4x)    |
| 100        | 11000       | 110000 (9.8x) | 150000 (12.9x) | 17000             | 240000 (13.9x) | 470000 (26.9x)    |
| 300        | 3700        | 100000 (27.5x) | 120000 (34.5x) | 4100              | 190000 (47.4x) | 310000 (76.5x)    |
| 1000       | 450         | 72000 (157.8x) | 85000 (185.8x) | 460               | 100000 (230.9x) | 130000 (300.2x)   |
| 3000       | 47          | 44000 (933.3x) | 49000 (1035.2x) | 47                | 56000 (1183.2x) | 64000 (1346.1x)   |

**Subtraction (x-y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 17000       | 89000 (5.1x) | 100000 (6.2x) | 36000             | 190000 (5.3x) | 320000 (8.7x)     |
| 30         | 16000       | 88000 (5.3x) | 110000 (6.6x) | 32000             | 190000 (5.9x) | 320000 (10.1x)    |
| 100        | 11000       | 68000 (6.1x) | 79000 (7.1x) | 16000             | 130000 (7.8x) | 180000 (11.3x)    |
| 300        | 3400        | 66000 (19.2x) | 77000 (22.4x) | 3800              | 120000 (31.9x) | 170000 (44.2x)    |
| 1000       | 400         | 54000 (134.2x) | 62000 (154.2x) | 410               | 88000 (215.5x) | 110000 (270.8x)   |
| 3000       | 54          | 36000 (680.0x) | 41000 (770.0x) | 54                | 51000 (943.0x) | 58000 (1076.9x)   |

**Multiplication (x\*y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 25000       | 130000 (5.2x) | 170000 (7.0x) | 57000             | 290000 (5.1x) | 570000 (10.1x)    |
| 30         | 23000       | 130000 (5.7x) | 170000 (7.7x) | 48000             | 280000 (5.9x) | 570000 (11.9x)    |
| 100        | 12000       | 97000 (7.7x) | 120000 (9.5x) | 17000             | 160000 (9.3x) | 240000 (13.4x)    |
| 300        | 2800        | 42000 (15.0x) | 45000 (16.2x) | 2900              | 51000 (17.1x) | 55000 (18.7x)     |
| 1000       | 300         | 7900 (25.8x) | 8000 (26.1x) | 310               | 8200 (26.5x)  | 8300 (26.9x)      |
| 3000       | 39          | 1300 (35.0x) | 1300 (35.1x) | 39                | 1300 (35.2x)  | 1300 (35.4x)      |

**Division (x/y)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 22000       | 89000 (4.0x) | 110000 (5.1x) | 47000             | 180000 (3.8x) | 300000 (6.5x)     |
| 30         | 20000       | 80000 (3.9x) | 100000 (5.0x) | 40000             | 160000 (4.1x) | 250000 (6.3x)     |
| 100        | 14000       | 58000 (4.0x) | 70000 (4.8x) | 21000             | 89000 (4.1x)  | 110000 (5.1x)     |
| 300        | 4500        | 18000 (4.1x) | 19000 (4.3x) | 5000              | 21000 (4.2x)  | 22000 (4.4x)      |
| 1000       | 540         | 2400 (4.5x) | 2400 (4.5x)  | 550               | 2400 (4.5x)   | 2400 (4.5x)       |
| 3000       | 71          | 290 (4.0x) | 290 (4.1x)   | 71                | 290 (4.0x)    | 290 (4.1x)        |

**Square root (x^0.5)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 14000       | 43000 (3.0x) | 49000 (3.5x) | 29000             | 110000 (4.0x) | 120000 (4.3x)     |
| 30         | 12000       | 35000 (2.9x) | 40000 (3.3x) | 22000             | 94000 (4.2x)  | 100000 (4.6x)     |
| 100        | 6200        | 25000 (4.0x) | 27000 (4.4x) | 8200              | 52000 (6.4x)  | 55000 (6.7x)      |
| 300        | 1400        | 12000 (8.9x) | 13000 (9.4x) | 1400              | 17000 (11.6x) | 18000 (12.8x)     |
| 1000       | 140         | 2800 (19.1x) | 2800 (19.5x) | 140               | 3000 (21.0x)  | 3000 (21.0x)      |
| 3000       | 15          | 400 (25.3x) | 400 (25.8x)  | 15                | 410 (26.0x)   | 410 (26.1x)       |

**Integer power (x^5)**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 2300        | 75000 (31.9x) | 95000 (40.3x) | 3900              | 120000 (31.9x) | 180000 (47.0x)    |
| 30         | 1600        | 53000 (31.4x) | 62000 (37.1x) | 2500              | 82000 (32.7x) | 98000 (39.4x)     |
| 100        | 460         | 41000 (90.4x) | 46000 (101.9x) | 540               | 82000 (152.5x) | 100000 (189.7x)   |
| 300        | 47          | 19000 (420.8x) | 21000 (449.2x) | 48                | 26000 (535.6x) | 27000 (572.7x)    |
| 1000       | 2           | 3700 (1817.8x) | 3700 (1834.7x) | 2                 | 3800 (1908.0x) | 3900 (1927.0x)    |

**Exponential function (exp(x))**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 6500        | 38000 (5.9x) | 41000 (6.3x) | 11000             | 70000 (5.9x)  | 94000 (7.9x)      |
| 30         | 4900        | 29000 (5.9x) | 30000 (6.2x) | 7800              | 50000 (6.4x)  | 58000 (7.4x)      |
| 100        | 1200        | 11000 (8.7x) | 11000 (8.8x) | 1500              | 14000 (9.8x)  | 15000 (10.4x)     |
| 300        | 110         | 1700 (15.8x) | 1700 (15.8x) | 110               | 1800 (16.2x)  | 1800 (16.2x)      |
| 1000       | 4           | 120 (28.8x) | 120 (28.9x)  | 4                 | 120 (28.8x)   | 120 (28.7x)       |

**Natural logarithm (log(x))**
| **digits** | **Decimal** | **mpf** |  **raw mpf** | **Decimal+psyco** | **mpf+psyco** | **raw mpf+psyco** |
|:-----------|:------------|:--------|:-------------|:------------------|:--------------|:------------------|
| 15         | 3300        | 13000 (4.1x) | 17000 (5.3x) | 5800              | 28000 (4.9x)  | 37000 (6.4x)      |
| 30         | 2500        | 9800 (3.9x) | 11000 (4.6x) | 3800              | 19000 (5.0x)  | 23000 (6.1x)      |
| 100        | 700         | 4500 (6.5x) | 4900 (7.1x)  | 830               | 7300 (8.8x)   | 7700 (9.3x)       |
| 300        | 80          | 1000 (13.3x) | 1000 (13.7x) | 83                | 1200 (14.8x)  | 1200 (15.2x)      |
| 1000       | 3           | 100 (26.7x) | 100 (26.8x)  | 3                 | 100 (26.9x)   | 100 (27.0x)       |