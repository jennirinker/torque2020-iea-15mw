# -*- coding: utf-8 -*-
"""Plot steady-state comparison
"""
import os
import warnings
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from _inputs import (steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf, prebend, i_thr, i_trq, fig_dir)
from _utils import read_steady


plot_keys = [('RotSpeed', i_gspd, 'GenSpeed [rpm]', 1),
             ('BldPitch1', i_pit, 'Pitch [deg]', 1),
             ('GenPwr', i_pow, 'Power [MW]', 1e-3),
             ('RootMyb1', i_flp, 'Flapwise [MNm]', 1e-3),
#             ('RootMEdg1', 'edge', 'Edgewise [MNm]', 1e-3),
             ('TwrBsMyt', i_tbfa, 'TwrBs FA [MNm]', 1e-3),
             ('TipDxb1', i_tipf, 'TipDefl [m]', 1)]
alpha = 0.8

# make figure
pltprms = {'font.size': 10, 'axes.labelsize': 10}
with plt.rc_context(pltprms):
    fig, axs = plt.subplots(2, 3, num=3, figsize=(9, 4), clear=True)

# plot stuff
for i, (fastname, h2name) in enumerate(model_keys):
    # make paths
    h2_path = steady_dir + f'{h2name}_Steady_stats.csv'
    fast_path = steady_dir + f'IEA15MW_torque_steady_{fastname}_stats.yaml'
    # load data
    h2_df = read_steady(h2_path)
    fast_df = read_steady(fast_path)
    for j, (fast_key, h2_chan, label, scl) in enumerate(plot_keys):
        ax = axs[j//3, j%3]
        # update fast_keys and scaling for beamdyn
        fst_scl, h2scl = scl, scl
        if 'GenPwr' in fast_key:
            h2scl *= 1e-3  # hawc2 is in W
        elif 'RootM' in fast_key:
            h2scl *= -1  # hawc2 flap is negative
            if 'BD' in fastname:
                fast_key = 'B1' + fast_key[:6] + 'r'
                fst_scl *= 1e-3  # beamdyn outputs Nm
        elif 'TipDx' in fast_key and 'BD' in fastname:  # tip deflection
            fast_key = 'B1TipTDxr'
        # isolate data
        fast_wsp, fast_data = fast_df.loc['mean', ['Wind1VelX', fast_key]]
        h2_wsp, h2_data = h2_df.loc['mean'][[str(i_uhub), str(h2_chan)]].values.T
        # scale and offset
        h2_data *= h2scl
        fast_data = fst_scl * np.array(fast_data)
        if 'Tip' in fast_key:
            h2_data += prebend
        elif 'TwrBsMyt' in fast_key:
            h2_data *= (150-15)/150
        # plot data
        c1, c2 = None, None
        if i > 0:
            c1, c2 = l1.get_color(), l2.get_color()
        l1, = ax.plot(fast_wsp, fast_data, label=['ElastoDyn', 'BeamDyn'][i],
                      linestyle=['-', '--'][i], c=c1, alpha=alpha)
        l2, = ax.plot(h2_wsp, h2_data, label=['H2-CNT', 'H2-FPM'][i],
                      linestyle=['-', '--'][i], c=c2, alpha=alpha)
        ax.grid('on')
        if i == 0:
            ax.set_title(label, fontsize=10)
        if j // 3:
            ax.set_xlabel('Wind speed [m/s]')
# prettify
plt.tight_layout(rect=[0.03, 0, 1, 1])
fig.axes[2].legend(fontsize=9, loc=4)

# save figure
figname = os.path.basename(__file__).replace('.py', '.png')
fig.savefig(fig_dir + figname, dpi=150)
