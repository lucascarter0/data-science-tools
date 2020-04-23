# Power Analysis
These scripts compare the statistical power of different hypothesis tests against various distributions and effect sizes. In hypothesis testing, statistical power is a measure of the probability of successfully rejecting a null hypothesis, given one exists. It is the inverse of the probability of a Type II error, which is the probability of accepting the null hypothesis when the alternative hypothesis is true. These tables can be used as part of designing a hypothesis test.

Relevant information contained in the contour plots:
- For a fixed sample size and known distribution, which hypothesis test has the strongest statistical power?
- For a known distribution and expected effect size, how many samples are needed to achieve a desired statistical power?

**It should be noted that "effect size" in these examples is a bit of an abuse of notation. The effect size in these plots is not based on the hypothesis test itself. It is simply a shift in the mean value of one distribution relative to another. This was done to force the hypothesis test result that was intended through the Monte Carlo iterations. **

## Gaussian Distribution
T-Test is most powerful of the compared tests for Gaussian distribution. Not surprising, since it is a parametric test vs non-parametric tests.
Two Sample T-Test |  Two Sample KS-Test | Wilcoxon Signed-Rank Test | Kruskal-Wallis H Test | Mann-Whitney U Test
:-------------------------:|:-------------------------:| :-------------------------: | :-------------------------:| :-------------------------: 
![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/gaussian_ttest.png) |  ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/gaussian_ks.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/gaussian_wilcoxon.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/gaussian_mannwhitney.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/gaussian_kruskalwallis.png)

## Binomial Distribution
### McNemar Test
![McNemar Test.](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/binomial_mcnemar.png)

## Exponential Distribution
The Mann-Whitney U Test appears to be the most powerful non-parametric test for the exponential distribution.
Two Sample KS-Test | Wilcoxon Signed-Rank Test | Kruskal-Wallis H Test | Mann-Whitney U Test
:-------------------------:| :-------------------------: | :-------------------------:| :-------------------------: 
![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/exponential_ks.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/exponential_wilcoxon.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/exponential_mannwhitney.png) | ![](https://github.com/lucascarter0/data-science-tools/blob/master/power_analysis/exponential_kruskalwallis.png)
