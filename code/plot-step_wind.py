# -*- coding: utf-8 -*-
"""Plot step wind
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from _inputs import (step_dir, model_keys, i_gspd, i_pit, i_gtrq, fig_dir)
from _utils import read_step

plot_keys = [('GenSpeed', i_gspd,'Generator Speed [rpm]', 1),
             ('BldPitch1', i_pit, 'Blade Pitch [deg]', 1),
             ('GenTq', i_gtrq, 'Generator Torque [MNm]', -1e-6)]
# ('GenPwr', i_pow, 1e-3)
alpha = 0.9

#%% load data
print('Loading data...')

step_data = []
steady_data =[]
for i, (fastname, h2name) in enumerate(model_keys):
    # path names
    fast_path = step_dir + f'IEA15MW_step_torque_{fastname}_0.outb'
    h2_path = step_dir + (f'iea_15mw_{h2name}_rwt_step.sel').lower()
    # load data
    fast_df = read_step(fast_path, usecols=[t[0] for t in plot_keys])
    h2_df = read_step(h2_path)
    # add to list
    step_data.append([fast_df, h2_df])
    del fast_df, h2_df

#%% plot data

pltprms = {'font.size': 10, 'axes.labelsize': 10}
with plt.rc_context(pltprms):
    fig, axs = plt.subplots(2, len(plot_keys), num=8, clear=True, figsize=(9, 4))

for i, (fastname, h2name) in enumerate(model_keys):
    fast_df, h2_df = step_data[i]
    
    for j, (fast_key, h2_chan, label, h2scl) in enumerate(plot_keys):
        # get axes
        ax = axs[i, j]
        ax.grid('on')
        # isolate and scale step data
        print(fast_key)
        fast_data = fast_df[fast_key]
        h2_data = h2_df[h2_chan] * h2scl
        if 'GenTq' in fast_key:
            fast_data = fast_data * 1e-3
        # plot
        c1, c2 = None, None
        if i > 0:
            c1, c2 = l1.get_color(), l2.get_color()
        l1, = ax.plot(fast_df['Time'], fast_data, label=['ElastoDyn', 'BeamDyn'][i],
                      linestyle=['-', '--'][i], c=c1, alpha=alpha)
        l2, = ax.plot(h2_data, label=['H2-CNT', 'H2-FPM'][i],
                      linestyle=['-', '--'][i], c=c2, alpha=alpha)
        ax.set_xlim([200, h2_data.index[-1]])
        if i == 0:
            ax.set_title(label, fontsize=10)
        else:
            ax.set_xlabel('Time [s]')

axs[0, -1].legend(loc=4)
axs[1, -1].legend(loc=4)
plt.tight_layout()

# save figure
figname = os.path.basename(__file__).replace('.py', '.png')
fig.savefig(fig_dir + figname, dpi=150)
