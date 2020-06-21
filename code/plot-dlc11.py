# -*- coding: utf-8 -*-
"""Plot DLC 1.1 for paper
"""
import os
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from _inputs import (dlc11_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf, prebend, i_thr, i_trq, fig_dir,
                     i_ywbr)
from _utils import read_dlc11


plot_keys = [('BldPitch1', i_pit, 'Blade pitch [deg]', 1),
             ('GenSpeed', i_gspd, 'Generator speed [rpm]', 1),
             ('GenPwr', i_pow, 'Power [MW]', 1e-3),
             ('RtAeroFxh', i_thr, 'Thrust [MN]', 1e-6),
             ('RootMyb1', i_flp, 'Flapwise BRM [MNm]', 1e-3),
             ('RootMxb1', i_edg, 'Edgewise BRM [MNm]', 1e-3),
             ('TwrBsMyt', i_tbfa, 'Tower-base fore-aft [MNm]', 1e-3),
             ('YawBrMyp', i_ywbr, 'Yaw-bearing pitch moment [MNm]', 1e-3),
             ('TipDxb1', i_tipf, 'Tip deflection [m]', 1)]  # fast, h2chan, h2scl
alpha = 0.5
darks = cm.get_cmap('tab20')(range(0, 20, 2))
lights = cm.get_cmap('tab20')(range(1, 20, 2))

# keys = [('GenSpeed', 9, 'Generator speed [rpm]', 30/np.pi, 1),
#         ('BldPitch1', 3, 'Blade pitch [deg]', 1, 1),
#         ('GenPwr', 90, 'Power [MW]', 1e-3, 1e-3),
#         ('RootMyb1', 25, 'Flapwise BRM [MNm]', -1, 1e-3),
#         ('RootMxb1', 26, 'Edgewise BRM [MNm]', 1, 1e-3),
#         ('RootMzc1', 27, 'Torsion BRM [MNm]', -1, -1e-3),
#         ('RotThrust', 12, 'Rotor thrust [MN]', 1, 1e-3),
#         ('YawBrMyp', 19, 'Yaw-bearing pitch moment [MNm]', 1, 1e-3),
#         ('TwrBsMyt', 16, 'Tower-base fore-aft [MNm]', 1, 1e-3),
#         ('TwrBsMxt', 17, 'Tower-base side-side [MNm]', 1, 1e-3),
#         ('TwrBsMzt', 18, 'Tower-base  torsion [MNm]', -1, 1e-3),
#         ('TipDxc1', 39, 'OoP tip deflection [m]', 1, 1),
# #        ('TipDxc1', 48, 'OoP tip deflection [m]', 1, 1),
# #        ('TipDyc1', 38, 'IP tip deflection [m]', -1, -1),
#         ]

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
        fig, axs = plt.subplots(3, 3, figsize=(9, 6), clear=True, num=4+i)
    for j, (fast_key, h2_chan, label, scl) in enumerate(plot_keys):
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
        # isolate data
        fast_wsps = fast_df.loc['mean', 'Wind1VelX']
        fast_means = fast_df.loc['mean', fast_key]
        fast_stds = fast_df.loc['std', fast_key]
        h2_wspss = h2_df.loc[h2_df.channel_nr == i_uhub, 'mean']
        h2_means = h2_df.loc[h2_df.channel_nr == h2_chan, 'mean']
        h2_stds = h2_df.loc[h2_df.channel_nr == h2_chan, 'std']
        # scale and offset
        fast_means = np.array(fast_means) * fst_scl
        fast_stds = np.array(fast_stds) * fst_scl
        h2_means = h2_means * h2scl
        h2_stds = h2_stds * h2scl
        if 'Tip' in fast_key:
            h2_means += prebend
        elif 'TwrBsMyt' in fast_key:
            h2_means = h2_means * (150-15)/150
            h2_stds = h2_stds * (150-15)/150
        # plot data
        # ax.scatter(fast_wsps, fast_data, label='OF', s=6, alpha=0.4)
        # ax.scatter(h2_wsps, h2_data, label='H2', s=6, alpha=0.4)
        # ax.set_title(fast_key)
        ax.errorbar(fast_wsps, fast_means, yerr=fast_stds, fmt='o', zorder=5, capsize=5, 
                    alpha=alpha, mec=darks[0], ecolor=darks[0], mfc=lights[0],
                    label=['ElastoDyn', 'BeamDyn'][i])
        ax.errorbar(h2_wspss, h2_means, yerr=h2_stds, fmt='o', zorder=5, capsize=5, 
                    alpha=alpha, mec=darks[1], ecolor=darks[1], mfc=lights[1],
                    label=['H2-CNT', 'H2-FPM'][i])
        ax.set_title(label, fontsize=10)
    axs[0, -1].legend(loc=4)
    plt.tight_layout()
    # save figure
    figname = os.path.basename(__file__).replace('.py', f'_{i}.png')
    fig.savefig(fig_dir + figname, dpi=150)

