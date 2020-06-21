# -*- coding: utf-8 -*-
"""Compare step-wind responses
"""
import matplotlib.pyplot as plt
from _inputs import (step_dir, model_keys, i_gspd, i_pit, i_pow, i_gtrq, i_uhub)
from _utils import read_step


ed_only = False
plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('GenPwr', i_pow, 1e-3),
             ('GenTq', i_gtrq, -1e-3)]

#%% load data
print('Loading data...')

fig_ht, ny = 5, 2
if ed_only:
    model_keys = [model_keys[0]]
    fig_ht, ny = 3, 1

data = []
for i, (fastname, h2name) in enumerate(model_keys):
    # path names
    fast_path = step_dir + f'IEA15MW_step_torque_{fastname}_0.out'
    h2_path = step_dir + (f'iea_15mw_{h2name}_rwt_step.sel').lower()
    # load data
    fast_df = read_step(fast_path, usecols=[t[0] for t in plot_keys])
    h2_df = read_step(h2_path)
    # add to list
    data.append([fast_df, h2_df])
    del fast_df, h2_df

#%% plot data

fig, axs = plt.subplots(ny, len(plot_keys), num=2, clear=True, figsize=(10, fig_ht))

for i, (fastname, h2name) in enumerate(model_keys):
    fast_df, h2_df = data[i]
    for j, (fast_key, h2_chan, h2scl) in enumerate(plot_keys):
        # get axes
        if ed_only:
            ax = axs[j]
        else:
            ax = axs[i, j]
        # update keys for beamdayn
        if 'RootM' in fast_key and '_BD_' in fast_path:
            fast_key = 'B1RootMyr'
            h2scl = -1e3
        # isolate and scale data
        fast_data = fast_df[fast_key]
        h2_data = h2_df[h2_chan] * h2scl
        # plot
        ax.plot(fast_data, label='OF')
        ax.plot(h2_data, label='H2')
        ax.set_title(f'{fastname}, {fast_key}')
        ax.set_xlim([200, h2_data.index[-1]])

ax.legend()
plt.tight_layout()
