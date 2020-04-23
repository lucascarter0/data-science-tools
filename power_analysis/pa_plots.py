# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:09:21 2018

@author: lucas
"""

from scipy import stats
import numpy as np
from statsmodels.stats.contingency_tables import mcnemar
from power_analysis import Test, montecarlo_sweep, contour_plot, contingency_table


# Define range of effect sizes for all cases
effect = np.linspace(0.1, 1, num=20)


# Create test class
gauss = Test()

# Distribution is Gaussian
gauss.dist = lambda m,n : np.random.normal(loc=m, size=(n,))

# mean value of Gaussian
m = np.array([0])



#Compute power statistic for two sample KS hypothesis test
gauss.hypothesis = stats.ks_2samp
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of KS Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size',
             title=title, save_label='gaussian_ks')

# Repeat with two sample t-test (assumes equal variance)
gauss.hypothesis = stats.ttest_ind
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of T-Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             title=title, save_label='gaussian_ttest')


# Repeat with Wilcoxon signed-rank test
gauss.hypothesis = stats.wilcoxon
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Wilcoxon Signed-Rank Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             save_label='gaussian_wilcoxon', title=title)


# Repeat with Mann-Whitney U test
gauss.hypothesis = stats.mannwhitneyu
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Mann-Whitney U Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             save_label='gaussian_mannwhitney', title=title)


# Repeat with Kruskal-Wallis H test
gauss.hypothesis = stats.kruskal
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Kruskal-Wallis H Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             save_label='gaussian_kruskalwallis', title=title)



# Binomial Distribution
binom = Test()
binom.dist = lambda p, n : np.random.binomial(1, p, size=(n,))
binom.hypothesis = lambda a,b, : mcnemar(contingency_table(a,b), exact=True)

# mean probability of success
m = np.array([0.5])

#Compute power statistic
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of McNemar Test\n'\
'Binomial Distribution ($p$=0.5)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             title=title, save_label='binomial_mcnemar')








# Exponential Distribution
# Create test class
exp = Test()

# Distribution is Exponential
exp.dist = lambda m,n : np.random.exponential(scale=m, size=(n,))
# Two sample KS hypothesis test
exp.hypothesis = stats.ks_2samp

# Scale of exponential
m = np.array([1])



#Compute power statistic
power = montecarlo_sweep(exp, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of KS Test\n'\
'Exponential Distribution ($\lambda$=1)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(exp, effect, power, ylabel='Effect Size',
             title=title, save_label='exponential_ks')


# Repeat with Wilcoxon signed rank test
exp.hypothesis = stats.wilcoxon
power = montecarlo_sweep(exp, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Wilcoxon Signed-Rank Test\n'\
'Exponential Distribution ($\lambda$=1)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(exp, effect, power, ylabel='Effect Size', 
             save_label='exponential_wilcoxon', title=title)


# Repeat with Mann-Whitney U test
exp.hypothesis = stats.mannwhitneyu
power = montecarlo_sweep(exp, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Mann-Whitney U Test\n'\
'Exponential Distribution ($\lambda$=1)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(exp, effect, power, ylabel='Effect Size', 
             save_label='exponential_mannwhitney', title=title)



# Plot results
exp.hypothesis = stats.kruskal
power = montecarlo_sweep(exp, means=m, effect_sizes=effect)

title = 'Statistical Power of Kruskal-Wallis H Test\n'\
'Exponential Distribution ($\lambda$=1)\n'\
'Various Effect Sizes (Percentage of Original Scale Value)'
contour_plot(exp, effect, power, ylabel='Effect Size', 
             save_label='exponential_kruskalwallis', title=title)
