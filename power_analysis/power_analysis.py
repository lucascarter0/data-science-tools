# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:53:17 2020

@author: lucas
"""

import numpy as np
import matplotlib.pyplot as plt

class Test:
    
    def __init__(self):
        
        # Number of iterations for Monte Carlo sampling
        self.iterations = 500
        
        # Array of sample sizes for Monte Carlo sampling
        self.samples = np.linspace(10,200,num=50,dtype=int)
        
        # Significance level (95% Confidence Interval)
        self.alpha = 0.05
        
        self.dist = None
        self.hypothesis = None
        
    def significant(self, a, b):
        assert self.hypothesis is not None, "Hypothesis test not defined"
        return self.hypothesis(a,b).pvalue <= self.alpha
    
    def sample(self, mean, effect, size):
        assert self.dist is not None, "Data distribution not defined"
        a = self.dist(mean, size)
        b = self.dist(mean-effect, size)
        return a,b



# Calculate Contingency Table for McNemar Test
def contingency_table(a,b):
    assert len(a) == len(b)
    t = np.array([[a.sum() + b.sum(), 
                   a.sum() + (len(b)-b.sum())],
                 [(len(a)-a.sum()) + b.sum(), 
                  (len(a)-a.sum()) + (len(b)-b.sum())]])
    return t



# Calculate Power Statistic Across Varying Parameters
# Using Monte Carlo analysis to calculate power statistic
def montecarlo_sweep(t, means, effect_sizes):
    power = np.array([])
    for m in means:
        for e in effect_sizes:
            for nruns in t.samples:
                correct_result = 0
                for ii in np.arange(1,t.iterations):
                    a,b = t.sample(mean=m, effect=e, size=nruns)
                
                    if t.significant(a,b):
                        correct_result += 1
                power = np.append(power, correct_result/t.iterations)
    return power


# Plot results against sample size and y-axis value. Power statistic 
# plotted as color contour
def contour_plot(t, y, z, ylabel='', title='', save_label=None):
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    X,Y = np.meshgrid(t.samples, y)
    
    z = z.reshape(len(y), len(t.samples))
    
    cs = ax.contourf(X,Y,z, 15, vmin=0.25, vmax=1)
    
    ax.set_xlabel('Sample Size')
    ax.set_ylabel(ylabel)
    
    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel('Statistical Power')
    
    ax.set_title(title)
    fig.tight_layout()
    
    if save_label:
        fig.savefig('{}.png'.format(save_label), dpi=600)
    




