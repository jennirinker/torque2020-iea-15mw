# -*- coding: utf-8 -*-
"""compare steady states
"""
import matplotlib.pyplot as plt
from _inputs import (steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf, prebend, i_thr, i_trq)
from _utils import read_steady


ed_only = False  # ElastoDyn-only results
plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('RtAeroFxh', i_thr, 1e3),
             ('GenTq', i_gtrq, -1e-3), ('RootMyb1', i_flp, -1), ('RootMxb1', i_edg, 1),
             ('TwrBsMyt', i_tbfa, 1), ('TipDxb1', i_tipf, 1)]  # fast, h2chan, h2scl
# ('GenPwr', i_pow, 1e-3) , ('TipDxb1', i_tipf, 1) ('RtAeroMxh', i_trq, 1e3)

# --------------------------------------------------------------------------------------

fig_ht, ny = 8, 4
if ed_only:
    model_keys = [model_keys[0]]
    fig_ht, ny = 4, 2

# can plot up to 8 channels
fig, axs = plt.subplots(ny, 4, figsize=(12, fig_ht), clear=True, num=1)

for i, (fastname, h2name) in enumerate(model_keys):
    # make paths
    h2_path = steady_dir + f'{h2name}_Steady_stats.csv'
    fast_path = steady_dir + f'IEA15MW_torque_steady_{fastname}_stats.yaml'
    # load data
    h2_df = read_steady(h2_path)
    fast_df = read_steady(fast_path)
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
        fast_wsp, fast_data = fast_df.loc['mean', ['Wind1VelX', fast_key]]
        h2_wsp, h2_data = h2_df.loc['mean'][[str(i_uhub), str(h2_chan)]].values.T
        # scale and offset
        h2_data *= h2scl
        if 'Tip' in fast_key:
            h2_data += prebend
        elif 'TwrBsMyt' in fast_key:
            h2_data *= (150-15)/150
        # plot data
        ax.plot(fast_wsp, fast_data, label='OF')
        ax.plot(h2_wsp, h2_data, label='H2')
        ax.set_title(f'{fast_key},\n {h2name} vs. {fastname}')
    

    
axs[1, 1].legend()
plt.tight_layout()