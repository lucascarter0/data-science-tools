# Power Analysis
These scripts compare the statistical power of different hypothesis tests against various distributions and effect sizes. In hypothesis testing, statistical power is a measure of the probability of successfully rejecting a null hypothesis, given one exists. It is the inverse of the probability of a Type II error, which is the probability of accepting the null hypothesis when the alternative hypothesis is true. These tables can be used as part of designing a hypothesis test.

Relevant information contained in the contour plots:
- For a fixed sample size and known distribution, which hypothesis test has the strongest statistical power?
- For a known distribution and expected effect size, how many samples are needed to achieve a desired statistical power?


## Gaussian Distribution
Two Sample T-Test |  Two Sample KS-Test | Wilcoxon Signed-Rank Test
:-------------------------:|:-------------------------:| :-------------------------:
![Two Sample T-Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/ttest_gaussian.png)
  |  ![Two Sample KS-Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/ks_gaussian.png)
| ![Wilcoxon Signed-Rank Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/wilcoxon_gaussian.png)
### Two Sample T-Test
![Two Sample T-Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/ttest_gaussian.png)
### Two Sample KS-Test
![Two Sample KS-Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/ks_gaussian.png)
### Wilcoxon Signed-Rank Test
![Wilcoxon Signed-Rank Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/wilcoxon_gaussian.png)

## Binomial Distribution
### McNemar Test
![McNemar Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/mcnemar_binomial.png)
