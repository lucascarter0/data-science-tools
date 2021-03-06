# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:44:40 2019

@author: Lucas Carter
"""

import support
import copy
import target_model as tgt
import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt
from filterpy.kalman import IMMEstimator as IMM



def init_ca_filter(dt, std):
    cafilter = KalmanFilter(dim_x=3, dim_z=1)
    cafilter.x = np.array([0., 0., 0.])
    cafilter.P *= 3
    cafilter.R *= std
    cafilter.Q = Q_discrete_white_noise(dim=3, dt=dt, var=0.02)
    cafilter.F = np.array([[1, dt, 0.5*dt*dt],
                           [0, 1,         dt], 
                           [0, 0,          1]])
    cafilter.H = np.array([[1., 0, 0]])
    return cafilter


    
def init_cv_filter(dt, std):
    cvfilter = KalmanFilter(dim_x = 2, dim_z=1)
    cvfilter.x = np.array([0., 0.])
    cvfilter.P *= 3
    cvfilter.R *= std**2
    cvfilter.Q = Q_discrete_white_noise(dim=2, dt=dt, var=0.02)
    cvfilter.F = np.array([[1, dt],
                           [0,  1]], dtype=float)
    cvfilter.H = np.array([[1, 0]], dtype=float)
    return cvfilter

def init_imm_filter(dt, std):
    kf1 = init_ca_filter(dt, std)
    kf2 = copy.deepcopy(kf1)  
    
    # Assume no process noise in first model 
    # (attempting to model CV while still carrying three states)
    kf1.Q *= 0
    
    mu_ = np.array([0.5, 0.5])
    transition_probability = np.array([[0.97, 0.03], [0.03, 0.97]])
    
    imm = IMM([kf1, kf2], mu_, transition_probability)
    return imm

   
    
dt = 0.1
sensor_std = 0.5

track2, zs2 = tgt.generate_data(60, sensor_std)
xs2 = track2[:, 0]
z_xs2 = zs2[:, 0]

cafilter  = init_ca_filter(dt, sensor_std)
cvfilter  = init_cv_filter(dt, sensor_std)
immfilter = init_imm_filter(dt, sensor_std)


xs_cv, xs_ca, xs_imm  = [], [], []

pv, pa = 0.5, 0.5 # Uninformed prior for MMAE

xs, probs, imm_prob = [],[],[]
for t, z in enumerate(z_xs2):
    
    # Track performance of CA in X only
    cafilter.predict()
    cafilter.update([z])
    xs_ca.append(cafilter.x[0])
    
    # Track performance of CV in X only
    cvfilter.predict()
    cvfilter.update([z])
    xs_cv.append(cvfilter.x[0])
    
    # Track performance of IMM
    immfilter.predict()
    immfilter.update([z])
    xs_imm.append(immfilter.x[0])
    imm_prob.append(immfilter.mu)
    
    
    # Compute MMAE estimate based on likelihood of both filters
    L_cv = cvfilter.likelihood * pv
    L_ca = cafilter.likelihood * pa
        
    pv = (L_cv) / (L_cv + L_ca)
    pa = (L_ca) / (L_cv + L_ca)
        
    x = (pv * cvfilter.x[0]) + (pa*cafilter.x[0])
    xs.append(x)
    probs.append([pv, pa])
        





#### Plot true target motion and noisy measurements
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(zs2[:,0], zs2[:,1], 
           c='k', alpha=0.25, label='Measurements')
ax.plot(track2[:,0], track2[:,1], 
        linewidth=3, c='k', label='True Target Motion')
support.set_labels(ax=ax, title='Motion of a Maneuvering Target',
                   x='X', y='Y')
ax.legend()
fig.tight_layout()
fig.savefig('true_motion.png', dpi=fig.dpi, bbox_inches='tight')





#### Plot comparison of CA and CV filters
fig, ax = plt.subplots(figsize=(12,8))
ax.plot(np.arange(0, len(xs2)*dt, dt), xs2, 
        linewidth=2,c='k',label='True X position')
ax.plot(np.arange(0, len(xs2)*dt, dt), xs_cv, 
        linewidth=2, label='CV Estimate')
ax.plot(np.arange(0, len(xs2)*dt, dt), xs_ca, 
        linewidth=2, label='CA Estimate')
support.set_labels(ax=ax, title='CV and CA performance at Tracking Motion in X',
                   x='Time (seconds)', y='X Position')
ax.legend()
fig.tight_layout()
fig.savefig('initial_performance.png', dpi=fig.dpi, bbox_inches='tight')


## Plot R^2 in two parts - 
## initial constant velocity and beginning of turn
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(10,6))

t = np.arange(len(xs2))[:120]
support.plot_r2((xs_cv - xs2)[t], dt=dt, ax=ax1)
support.plot_r2((xs_ca - xs2)[t], dt=dt, ax=ax1)

t = np.arange(len(xs2))[121:170]
support.plot_r2((xs_cv - xs2)[t], dt=dt, ax=ax2, t=t*dt)
support.plot_r2((xs_ca - xs2)[t], dt=dt, ax=ax2, t=t*dt)

fig.tight_layout()
for ax in [ax1, ax2]:
    ax.legend(['Constant Velocity Filter','Constant Acceleration Filter'])
    ax.set_ylim(bottom=0)
    ax.grid()
fig.savefig('initial_performance_R2.png', dpi=fig.dpi, bbox_inches='tight')



t = np.arange(len(xs2))[:]



#### Plot MMAE Performance

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10,8))

support.plot_r2((xs_cv - xs2)[t], dt=dt, ax=ax1)
support.plot_r2((xs_ca - xs2)[t], dt=dt, ax=ax1)
support.plot_r2((xs - xs2)[t], dt=dt, ax=ax1)
ax1.legend(['CV Only', 'CA Only', 'MMAE'])

support.plot_probs(np.asarray(probs)[t],dt=dt, ax=ax2)
support.set_labels(ax=ax2, title='Probability weights in MMAE Filter',
                   x='Time (seconds)', y = '$P$')
ax2.legend(['$P$(CV)', '$P$(CA)'])
fig.tight_layout()
fig.savefig('mmae_compare.png', dpi=fig.dpi, bbox_inches='tight')





#### Plot IMM Performance vs MMAE
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10,9))
support.plot_r2((xs_imm - xs2)[t], dt=dt, ax=ax1)
ax1.legend(['IMM Filter'])

support.plot_probs(np.asarray(imm_prob)[t],dt=dt, ax=ax2)
ax2.legend(['$P(CV)$' ,'$P(CA)$'])
support.set_labels(ax=ax2, title='Probability weights in IMM Filter',
                   x='Time (seconds)', y = '$P$')
fig.tight_layout()
fig.savefig('imm_compare.png', dpi=fig.dpi, bbox_inches='tight')





#### Comparing IMM vs MMAE
fig, ax = plt.subplots(nrows=1, figsize=(10,8))
support.plot_r2((xs - xs2)[t], dt=dt, ax=ax)
support.plot_r2((xs_imm - xs2)[t], dt=dt, ax=ax)
ax.legend(['MMAE Filter', 'IMM Filter'])
ax.grid()
fig.tight_layout()
fig.savefig('imm_mmae_compare.png', dpi=fig.dpi, bbox_inches='tight')
