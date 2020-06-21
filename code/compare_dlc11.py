# -*- coding: utf-8 -*-
"""Compare the DLC 1.1 calculations
"""
import matplotlib.pyplot as plt
from _inputs import dlc11_dir
from _utils import read_dlc11
from _inputs import (steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf, prebend)


ed_only = True
plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('GenPwr', i_pow, 1e-3) ,
             ('GenTq', i_gtrq, -1e-3), ('RootMyb1', i_flp, -1), ('RootMxb1', i_edg, 1),
             ('TwrBsMyt', i_tbfa, 1), ('TipDxb1', i_tipf, 1)]  # fast, h2chan, h2scl


fig_ht, ny = 8, 4
if ed_only:
    model_keys = [model_keys[0]]
    fig_ht, ny = 4, 2

# can plot up to 8 channels
fig, axs = plt.subplots(ny, 4, figsize=(12, fig_ht), clear=True, num=4)

fast_path = dlc11_dir + 'IEA15MW_torque_DLC11_ED_stats.yaml'
h2_path = dlc11_dir + 'NoFPM_notorsion_DLC11_statistics.h5'
i, fastname = 0, 'ED'

# fast_path = dlc11_dir + 'IEA15MW_torque_DLC11_BD_stats.yaml'
# h2_path = dlc11_dir + 'FPM_DLC11_statistics.h5'
# i, fastname = 0, 'BD'

fast_df = read_dlc11(fast_path)
h2_df = read_dlc11(h2_path)

fast_wsps = fast_df.loc['mean', 'Wind1VelX']
h2_wsps = h2_df.loc[h2_df.channel_nr == i_uhub, 'mean'].values

stat = 'mean'

for j, (fast_key, h2_chan, h2scl) in enumerate(plot_keys):
    # identify axis
    if ed_only:
        ax = axs[j//4, j % 4]
    else:
        ax = axs[2*(j//4) + i, j % 4]
    # update fast_keys and scaling for beamdyn
    if 'RootM' in fast_key and 'BD' in fastname:  # blade root moments
        fast_key = 'B1' + fast_key[:6] + 'r'
        h2scl *= 1e3
    elif 'TipDx' in fast_key and 'BD' in fastname:  # tip deflection
        fast_key = 'B1TipTDxr'
    # isolate data
    fast_data = fast_df.loc[stat, fast_key]
    h2_data = h2_df.loc[h2_df.channel_nr == h2_chan, stat]
    # scale and offset
    if stat in ['std', 'abs']:
        h2scl = abs(h2scl)
    h2_data *= h2scl
    if 'Tip' in fast_key and stat == 'mean':
        h2_data += prebend
    elif 'TwrBsMyt' in fast_key:
        h2_data *= (150-15)/150
    # plot data
    ax.scatter(fast_wsps, fast_data, label='OF', s=6, alpha=0.4)
    ax.scatter(h2_wsps, h2_data, label='H2', s=6, alpha=0.4)
    ax.set_title(fast_key)
ax.legend()
plt.tight_layout()

