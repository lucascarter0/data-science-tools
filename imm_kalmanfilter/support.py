# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:03:22 2019

@author: Lucas Carter
"""

import numpy as np
import matplotlib.pyplot as plt

#### Credit to Kalman and Bayesian Filtering in Python by R. Labbe
#### for set_labels. These utilities helped save
#### time in plotting filter performance

def set_labels(ax=plt, title=None, x=None, y=None):
    """ helps make code in book shorter. Optional set title, xlabel and ylabel
    """
    if x is not None:
        ax.set_xlabel(x)
    if y is not None:
        ax.set_ylabel(y)
    if title is not None:
        ax.set_title(title)
    ax.grid()
        



def plot_res(res, dt=1,ax=plt):
    t = np.arange(0, len(res)*dt, dt)
    ax.plot(t, res,linewidth=2)
    if ax is plt:
        plt.xlabel('time (sec)')
        plt.ylabel('residual')
        plt.title('residuals')
        plt.show()
    else:
        ax.set_xlabel('time (sec)')
        ax.set_ylabel('residual')
        ax.set_title('Residual')
    ax.grid()
    
    
    
    
def plot_r2(res, dt=1, ax=plt, t=None):
    if t is None:
        t = np.arange(0, len(res)*dt, dt)
    r2 = np.power(res,2)
    ax.plot(t, r2,linewidth=3)
    if ax is plt:
        plt.xlabel('Time (sec)')
        plt.ylabel('$R^2$')
        plt.title('$R^2$ vs Time')
        plt.show()
    else:
        ax.set_xlabel('Time (sec)')
        ax.set_ylabel('$R^2$')
        ax.set_title('$R^2$ vs Time')
    ax.grid()
    
    
    
def plot_probs(probs, dt=1,ax=plt):
    t = np.arange(0, len(probs)*dt, dt)
    ax.plot(t, probs, linewidth=3)

    
    
