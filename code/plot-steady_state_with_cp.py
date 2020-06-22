# -*- coding: utf-8 -*-
"""Plot steady-state comparison for paper
"""
import os
import warnings
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from _inputs import (steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf, prebend, i_thr, i_trq, fig_dir,
                     fast_labels, h2_labels, i_ywbr)
from _utils import read_steady


plot_keys = [('RotSpeed', i_gspd, 'Generator Speed [rpm]', 1),
             ('BldPitch1', i_pit, 'Blade Pitch [deg]', 1),
             ('GenPwr', i_pow, 'Generator Power [MW]', 1e-3),
#             ('RootMEdg1', 'edge', 'Edgewise [MNm]', 1e-3),
             ('RtAeroCp', 500, 'Cp [-]', 1),
             ('RtAeroCt', 600, 'Ct [-]', 1),
             ('YawBrMyp', i_ywbr, 'Yaw-Bearing Pitch Moment [MNm]', 1e-3),
             ('TwrBsMyt', i_tbfa, 'Tower Base Fore-Aft Moment [MNm]', 1e-3),
             ('RootMyb1', i_flp, 'Flapwise Root Moment [MNm]', 1e-3),
             ('TipDxb1', i_tipf, 'Flapwise Tip Deflection [m]', 1)]
alpha = 0.8
bd_maxwsp = 25#20.1  # cutoff for BeamDyn frequencies
A = np.pi * 120**2

# make figure
pltprms = {'font.size': 10, 'axes.labelsize': 10}
with plt.rc_context(pltprms):
    fig, axs = plt.subplots(3, 3, num=13, figsize=(9, 6), clear=True)

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
        elif 'RtAeroCt' == fast_key:
            thrust = h2_df.loc['mean', str(i_thr)].values * 1e3
            wsp = h2_df.loc['mean'][str(i_uhub)].values
            h2_df.loc['mean', str(h2_chan)] = thrust / (0.5 * 1.225 * A * wsp**2)
        elif 'RtAeroCp' == fast_key:
            power = h2_df.loc['mean', str(i_pow)].values
            wsp = h2_df.loc['mean'][str(i_uhub)].values
            h2_df.loc['mean', str(h2_chan)] = power / (0.5 * 1.225 * A * wsp**3)
        # isolate data
        fast_wsp = np.array(fast_df.loc['mean', 'Wind1VelX'])
        fast_data = np.array(fast_df.loc['mean', fast_key])
        h2_wsp, h2_data = h2_df.loc['mean'][[str(i_uhub), str(h2_chan)]].values.T
        # scale and offset
        h2_data *= h2scl
        fast_data = fst_scl * np.array(fast_data)
        if 'Tip' in fast_key:
            h2_data += prebend
        # if BD,ignore >20 m/s
        if 'BD' in fastname:
            fast_data = fast_data[fast_wsp < bd_maxwsp]
            fast_wsp = fast_wsp[fast_wsp < bd_maxwsp]
            h2_data = h2_data[h2_wsp < bd_maxwsp]
            h2_wsp = h2_wsp[h2_wsp < bd_maxwsp]
        # plot data
        c1, c2 = None, None
        if i > 0:
            c1, c2 = l1.get_color(), l2.get_color()
        l1, = ax.plot(fast_wsp, fast_data, label=fast_labels[i],
                      linestyle=['-', '--'][i], c=c1, alpha=alpha)
        l2, = ax.plot(h2_wsp, h2_data, label=h2_labels[i],
                      linestyle=['-', '--'][i], c=c2, alpha=alpha)
        ax.grid('on')
        # if fast_key == 'RtAeroCp':
        #     cpline = ax.plot(fast_wsp, 0.489*np.ones(fast_wsp.size), ':', '0.4', lw=2,
        #                       alpha=0.6, zorder=-2, label='Design Cp')
        #     ax.set_ylim([0, 0.51])
        if i == 0:
            ax.set_title(label, fontsize=10)
        if j // 6:
            ax.set_xlabel('Wind speed [m/s]')
        ax.set_xlim([3, bd_maxwsp])
# prettify
plt.tight_layout()
fig.axes[2].legend(fontsize=10, loc=4)
# axs[1, 0].legend([cpline[0]], ['Design Cp'], fontsize=10,
#                  bbox_to_anchor=(0.97, 0.7), loc='upper right', borderaxespad=0.)

# # save figure
figname = os.path.basename(__file__).replace('.py', '.png')
fig.savefig(fig_dir + figname, dpi=150)
