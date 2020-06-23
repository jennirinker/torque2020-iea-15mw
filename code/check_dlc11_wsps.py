# -*- coding: utf-8 -*-
"""Scatterplot the means and standard deviations of the hub-height wind speed.
These should ideally fall directly on a straight line.
Unfortunately, unable to do 1-to-1 mapping bc no filename info in yaml stats.
"""
import matplotlib.pyplot as plt
from _utils import read_dlc11, read_step
from _inputs import (dlc11_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq, i_edg, i_tipf)
from wisdem.aeroelasticse.Util.ReadFASTout import ReadFASToutFormat


ed_only = True


plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('GenPwr', i_pow, 1e-3) ,
             ('GenTq', i_gtrq, -1e-3), ('RootMyb1', i_flp, -1), ('RootMxb1', i_edg, 1),
             ('TwrBsMyt', i_tbfa, 1), ('TipDxb1', i_tipf, 1)]  # fast, h2chan, h2scl

# =================================================
# scatterplot mean and standard deviation of hh wsp

# fast_path = dlc11_dir + 'IEA15MW_torque_DLC11_ED_stats.yaml'
# h2_path = dlc11_dir + 'NoFPM_notorsion_DLC11_statistics.h5'

# fast_df = read_dlc11(fast_path)
# h2_df = read_dlc11(h2_path)

# fig, axs = plt.subplots(1, 2, figsize=(8, 3), clear=True, num=10)
# for i, stat in enumerate(['mean', 'std']):
#     fast_wsps = fast_df.loc[stat, 'Wind1VelX']
#     h2_wsps = h2_df.loc[h2_df.channel_nr == i_uhub, stat].values
#     axs[i].scatter(sorted(fast_wsps), sorted(h2_wsps))
#     axs[i].set_title(stat)
#     axs[i].set_xlabel('Fast hh wsp')
#     axs[i].set_ylabel('HAWC2 hh wsp')

# =================================================
# time series

h2_fpm = dlc11_dir + 'dlc11_wsp10_wdir000_s3004_FPM.sel'
h2_nt = dlc11_dir + 'dlc11_wsp10_wdir000_s3004_NoFPM_notorsion.sel'
h2df_fpm = read_step(h2_fpm)
h2df_nt = read_step(h2_nt)

fast_bd =  dlc11_dir + 'IEA15MW_torque_DLC11_BD_20.outb'
fast_ed = dlc11_dir + 'IEA15MW_torque_DLC11_ED_20.outb'
fast_bd_dict = ReadFASToutFormat(fast_bd, OutFileFmt=2)[0]
fast_ed_dict = ReadFASToutFormat(fast_ed, OutFileFmt=2)[0]
#%%
plt.figure(11, clear=True, figsize=(12, 4))
plt.plot(fast_bd_dict['Time'], fast_bd_dict['Wind1VelX'], label='BD')
plt.plot(fast_ed_dict['Time'], fast_ed_dict['Wind1VelX'], label='ED')
plt.plot(h2df_fpm[i_uhub], label='FPM')
plt.plot(h2df_nt[i_uhub], label='NoFPM_notors')
plt.legend()
plt.tight_layout()



