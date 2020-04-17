# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:09:21 2020

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
# Two sample KS hypothesis test
gauss.hypothesis = stats.ks_2samp

# mean value of Gaussian
m = np.array([0])



#Compute power statistic
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of KS Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size',
             title=title, save_label='ks_gaussian')

# Repeat with two sample t-test (assumes equal variance)
gauss.hypothesis = stats.ttest_ind
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of T-Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             title=title, save_label='ttest_gaussian')


# Repeat with two sample t-test (assumes equal variance)
gauss.hypothesis = stats.wilcoxon
power = montecarlo_sweep(gauss, means=m, effect_sizes=effect)

# Plot results
title = 'Statistical Power of Wilcoxon Signed-Rank Test\n'\
'Gaussian Distribution ($\mu$=0)\n'\
'Various Effect Sizes (Percentage of Original Mean Value)'
contour_plot(gauss, effect, power, ylabel='Effect Size', 
             save_label='wilcoxon_gaussian', title=title)






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
             title=title, save_label='mcnemar_binomial')
