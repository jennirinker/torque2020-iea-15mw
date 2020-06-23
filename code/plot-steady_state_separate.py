# -*- coding: utf-8 -*-
"""Plot steady-state, but separate for operational and loads
"""
import os
import warnings
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from _inputs import (steady_dir, model_keys, prebend, fig_dir, fast_labels, h2_labels,
                     plot_dict, i_uhub, i_thr, i_pow)
from _utils import read_steady


all_keys = [['GenSpeed', 'BldPitch1',  'GenPwr',
             'GenTq', 'RtAeroCp', 'RtAeroCt',
             ],
             ['TwrBsMyt', 'TwrBsMxt', 'YawBrMyp',
              'RootMyb1', 'YawBrMxp', 'TipDxb1',
              #'RootMyb1', 'RootMxb1', 'TipDxb1',
              ]]  # fast keys to plot
alpha = 0.8
maxwsp = 26  # cutoff for BeamDyn frequencies
A = np.pi * 120**2
save_fig = False
plot_gentq = False  # plot generator torque on tb ss plot?

# --------------------------------------------------------------------------------------


# plot stuff
for m in range(2):  # two plots
    # make figure
    pltprms = {'font.size': 10, 'axes.labelsize': 10}
    with plt.rc_context(pltprms):
        fig, axs = plt.subplots(2, 3, num=13+m, figsize=(9, 4), clear=True)
    plot_keys = all_keys[m]
    for i, (fastname, h2name) in enumerate(model_keys):
        # make paths
        h2_path = steady_dir + f'{h2name}_Steady_stats.csv'
        fast_path = steady_dir + f'IEA15MW_torque_steady_{fastname}_stats.yaml'
        # load data
        h2_df = read_steady(h2_path)
        fast_df = read_steady(fast_path)
        for j, fast_key in enumerate(plot_keys):
            h2_chan, label, scl = plot_dict[fast_key]
            ax = axs[j//3, j%3]
            # update fast_keys and scaling for beamdyn
            fst_scl, h2scl = scl, scl
            if 'GenPwr' in fast_key:
                h2scl *= 1e-3  # hawc2 is in W
            elif 'GenTq' in fast_key:
                h2scl *= -1e-3  # hawc2 is in Nm
            elif 'RootM' in fast_key:
                if 'My' in fast_key:
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
            elif fast_key == 'RtAeroFxh':
                fst_scl *= 1e-3
            # isolate data
            fast_wsp = np.array(fast_df.loc['mean', 'Wind1VelX'])
            fast_data = np.array(fast_df.loc['mean', fast_key])
            fast_stds = np.array(fast_df.loc['std', fast_key])
            h2_wsp = h2_df.loc['mean', str(i_uhub)].values
            h2_data = h2_df.loc['mean', str(h2_chan)].values
            h2_stds = h2_df.loc['std', str(h2_chan)].values
            # scale and offset
            h2_data *= h2scl
            h2_stds *= np.abs(h2scl)
            fast_data *= fst_scl
            fast_stds *= np.abs(fst_scl)
            if 'Tip' in fast_key:
                h2_data += prebend
            # if BD,ignore >20 m/s
            if 'BD' in fastname:
                fast_data = fast_data[fast_wsp < maxwsp]
                fast_stds = fast_stds[fast_wsp < maxwsp]
                fast_wsp = fast_wsp[fast_wsp < maxwsp]
                h2_data = h2_data[h2_wsp < maxwsp]
                h2_stds = h2_stds[h2_wsp < maxwsp]
                h2_wsp = h2_wsp[h2_wsp < maxwsp]
            # if 'TwrBsMxt' in fast_key:
            #     print('DELETE HACK!!!!')
            #     fast_data *= (144.695)/150
            # plot data
            c1, c2 = None, None
            if i > 0:
                c1, c2 = l1.get_color(), l2.get_color()
            l1, = ax.plot(fast_wsp, fast_data, label=fast_labels[i],
                          linestyle=['-', '--'][i], c=c1, alpha=alpha)
            l2, = ax.plot(h2_wsp, h2_data, label=h2_labels[i],
                          linestyle=['-', '--'][i], c=c2, alpha=alpha)
            ax.grid('on')
            if i == 0:
                ax.set_title(label, fontsize=10)
            if j // 6:
                ax.set_xlabel('Wind speed [m/s]')
            ax.set_xlim([3, maxwsp])
    # prettify
    plt.tight_layout()
    if m == 0:  # plot cp
        cpline = axs[1, 1].plot([3, 25],[0.489, 0.489], ':', c='0.6', lw=2, zorder=0)
        axs[1, 1].legend([cpline[0]], ['Design Cp'], fontsize=10, loc=3)
        axs[0, -1].legend(fontsize=10, loc=4)
    else:
        # plot generator torque on tower base ss
        if plot_gentq:
            fast_wsp = np.array(fast_df.loc['mean', 'Wind1VelX'])
            fast_data = np.array(fast_df.loc['mean', 'GenTq']) * 1e-3
            axs[0, 1].plot(fast_wsp, fast_data, ':', c='0.6', lw=2, zorder=0, label='GenTq')
        # add legend
        axs[0, 1].legend(fontsize=10, loc=4)
        # axs[-1, -1].set_visible(False)
        # axs[-1, 1].legend(fontsize=10,
        #                   bbox_to_anchor=(1.26, 1.0), loc='upper left', borderaxespad=0.)
    
    # save figure
    if save_fig:
        figname = os.path.basename(__file__).replace('.py', f'_{["oper", "loads"][m]}.png')
        fig.savefig(fig_dir + figname, dpi=150)
