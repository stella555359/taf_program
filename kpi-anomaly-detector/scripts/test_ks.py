#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test KS-Test for specific codes"""

from scipy.stats import ks_2samp
import numpy as np

# M55360C01139 - high variance
hist_vals = [-100.15,-100.4,-89.94,-102.66,-99.68,-99.23,-95.48, 
             -87.05,-103.0,-94.93,-74.93,-96.47,-103.49,-88.52,-91.12,-86.85,-101.42,-102.65]
curr_vals = [-92.24,-78.37,-100.73,-87.15,-82.13,-97.31,-102.03,-103.55,-105.3,-93.14,-76.48]

stat, p = ks_2samp(curr_vals, hist_vals)
print('M55360C01139:')
print(f'  History mean: {np.mean(hist_vals):.2f}, std: {np.std(hist_vals):.2f}')
print(f'  Current mean: {np.mean(curr_vals):.2f}, std: {np.std(curr_vals):.2f}')
print(f'  KS statistic: {stat:.4f}')
print(f'  p-value: {p:.4f}')
if p < 0.01:
    judgment = 'Regression'
elif p < 0.05:
    judgment = 'Suspicious'
else:
    judgment = 'Normal'
print(f'  KS-Test Judgment: {judgment}')
print()

# M55360C00141 - very stable
hist_vals2 = [-115.143,-115.124,-115.113,-115.108,-115.12,-115.132,-115.131, 
              -115.104,-115.141,-115.117,-115.112,-115.123,-115.099,-115.126,-115.07,-115.116,-115.103,-115.119]
curr_vals2 = [-115.117,-115.112,-115.075,-115.091,-115.08,-115.089,-115.077,-115.133,-115.081,-115.087,-115.068]

stat2, p2 = ks_2samp(curr_vals2, hist_vals2)
print('M55360C00141:')
print(f'  History mean: {np.mean(hist_vals2):.4f}, std: {np.std(hist_vals2):.4f}')
print(f'  Current mean: {np.mean(curr_vals2):.4f}, std: {np.std(curr_vals2):.4f}')
print(f'  KS statistic: {stat2:.4f}')
print(f'  p-value: {p2:.4f}')
if p2 < 0.01:
    judgment2 = 'Regression'
elif p2 < 0.05:
    judgment2 = 'Suspicious'
else:
    judgment2 = 'Normal'
print(f'  KS-Test Judgment: {judgment2}')
