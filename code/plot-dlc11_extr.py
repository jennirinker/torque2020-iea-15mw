# -*- coding: utf-8 -*-
"""Plot DLC 1.1 for paper
"""
import os
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from _inputs import (dlc11_dir, model_keys, prebend, fast_labels, h2_labels, plot_dict,
                     i_uhub, fig_dir)
from _utils import read_dlc11


plot_keys = ['BldPitch1', 'GenSpeed', 'GenPwr', 
             'RootMyb1', 'RootMxb1', 'TipDxb1',
             'TwrBsMyt', 'TwrBsMxt',
             ]  # fast_keys to plot
alpha = 0.6
darks = cm.get_cmap('tab20')(range(0, 20, 2))
lights = cm.get_cmap('tab20')(range(1, 20, 2))
bd_maxwsp = 21  # cutoff for BeamDyn frequencies
save_fig = False

# --------------------------------------------------------------------------

# plot stuff
for i, (fastname, h2name) in enumerate(model_keys):
    # make paths
    h2_path = dlc11_dir + f'{h2name}_DLC11_statistics.h5'
    fast_path = dlc11_dir + f'IEA15MW_torque_DLC11_{fastname}_stats.yaml'
    # load data
    h2_df = read_dlc11(h2_path)
    fast_df = read_dlc11(fast_path)
    # make figure
    # can plot up to 9 channels
    pltprms = {'font.size': 10, 'axes.labelsize': 10}
    with plt.rc_context(pltprms):
        fig, axs = plt.subplots(3, 3, figsize=(9, 6), clear=True, num=19+i)
    for j, fast_key in enumerate(plot_keys):
        h2_chan, label, scl = plot_dict[fast_key]
        # identify axes
        ax = axs[j//3, j % 3]
        ax.grid('on')
        # update fast_keys and scaling for beamdyn
        fst_scl, h2scl = scl, scl
        if 'GenPwr' in fast_key:
            h2scl *= 1e-3  # hawc2 is in W
        elif 'RootM' in fast_key:
            if 'RootMy' in fast_key:
                h2scl *= -1  # hawc2 flap is negative
            if 'BD' in fastname:
                fast_key = 'B1' + fast_key[:6] + 'r'
                fst_scl *= 1e-3  # beamdyn outputs Nm
        elif 'TipDx' in fast_key and 'BD' in fastname:  # tip deflection
            fast_key = 'B1TipTDxr'
        elif 'RtAeroFxh' in fast_key:
            h2scl = 1e-3
        h2stat = 'max'
        if h2scl < 0:
            h2stat = 'min'
        # isolate data
        fast_wsps = np.array(fast_df.loc['mean', 'Wind1VelX'])
        fast_maxs = np.array(fast_df.loc['max', fast_key])
        h2_wsps = h2_df.loc[h2_df.channel_nr == i_uhub, 'mean'].values
        h2_maxs = h2_df.loc[h2_df.channel_nr == h2_chan, h2stat].values
        # scale and offset
        fast_maxs = fast_maxs * fst_scl
        h2_maxs = h2_maxs * h2scl
        if 'Tip' in fast_key:
            h2_maxs += prebend
        # if BD,ignore >20 m/s
        if 'BD' in fastname:
            fast_maxs = fast_maxs[fast_wsps < bd_maxwsp]
            fast_wsps = fast_wsps[fast_wsps < bd_maxwsp]
            h2_maxs = h2_maxs[h2_wsps < bd_maxwsp]
            h2_wsps = h2_wsps[h2_wsps < bd_maxwsp]
        ax.plot(fast_wsps, fast_maxs, 'o',
                mfc=lights[0], mec=darks[0], zorder=1, alpha=alpha,
                label=fast_labels[i])
        ax.plot(h2_wsps, h2_maxs, 'o',
                mfc=lights[1], mec=darks[1], zorder=1, alpha=alpha,
                label=h2_labels[i])
        ax.set_title(label, fontsize=10)
    axs[-1, -1].set_visible(False)
    plt.tight_layout()
    axs[-1, 1].legend(bbox_to_anchor=(1.23, 1), loc='upper left', borderaxespad=0)
    # save figure
    if save_fig:
        figname = os.path.basename(__file__).replace('.py', f'_{fastname}.png')
        fig.savefig(fig_dir + figname, dpi=150)

