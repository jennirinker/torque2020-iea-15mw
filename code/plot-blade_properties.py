# -*- coding: utf-8 -*-
"""Compare the distributed blade properties
"""
import os
import matplotlib.pyplot as plt
from _utils import read_blade_dat
from _inputs import blade_len, fig_dir


bd_path = 'C:/Users/rink/git/IEA-15-240-RWT/OpenFAST/IEA-15-240-RWT/IEA-15-240-RWT_BeamDyn_blade.dat'
ed_path = 'C:/Users/rink/git/IEA-15-240-RWT/OpenFAST/IEA-15-240-RWT/IEA-15-240-RWT_ElastoDyn_blade.dat'
h2fpm_path = 'C:/Users/rink/git/IEA-15-240-RWT/HAWC2/FPM/data/IEA_15MW_RWT_Blade_st.dat'
h2nofpm_path = 'C:/Users/rink/git/IEA-15-240-RWT/HAWC2/NoFPM_notorsion/data/IEA_15MW_RWT_Blade_st_noFPM.dat'

alpha = 0.8
save_fig = False

# load dataframes
bd_df = read_blade_dat(bd_path, blade_len=blade_len)
ed_df = read_blade_dat(ed_path, blade_len=blade_len)
nofpm_df = read_blade_dat(h2nofpm_path, blade_len=blade_len)
fpm_df = read_blade_dat(h2fpm_path, blade_len=blade_len)

pltprms = {'font.size': 11, 'axes.labelsize': 13}
with plt.rc_context(pltprms):
    fig, axs = plt.subplots(2, 2, num=1, clear=True, figsize=(9, 4))


# ========================================================
ax = axs[0, 0]  # blade mass density
ed_key, bd_key, fpm_key, label = 'BMassDen', 'M_11', 'm', 'Blade mass density [kg/m]'

nofpm_plot = nofpm_df['m']

l1, = ax.plot(ed_df[ed_key], label='ElastoDyn', alpha=alpha)
l2, = ax.plot(nofpm_plot, label='H2-CNT', alpha=alpha)
ax.plot(bd_df[bd_key], c=l1.get_color(), linestyle='--', label='BeamDyn', alpha=alpha)
ax.plot(fpm_df[fpm_key], c=l2.get_color(), linestyle='--', label='H2-FPM', alpha=alpha)
ax.set_xlim([0, blade_len])
ax.grid('on')
ax.set_title(label)

# ========================================================
ax = axs[0, 1]  # flapwise stiffness
ed_key, bd_key, fpm_key, label = 'FlpStff', 'K_55', 'K_44', 'Flapwise stiffness [Nm$^2$]'

nofpm_plot = nofpm_df['E'] * nofpm_df['I_x']

l1, = ax.plot(ed_df[ed_key], label='ElastoDyn', alpha=alpha)
l2, = ax.plot(nofpm_plot, label='H2-CNT', alpha=alpha)
ax.plot(bd_df[bd_key], c=l1.get_color(), linestyle='--', label='BeamDyn', alpha=alpha)
ax.plot(fpm_df[fpm_key], c=l2.get_color(), linestyle='--', label='H2-FPM', alpha=alpha)
ax.set_xlim([0, blade_len])
ax.grid('on')
ax.set_title(label)

# ========================================================
ax = axs[1, 1]  # edgewise stiffness
ed_key, bd_key, fpm_key, label = 'EdgStff', 'K_44', 'K_55', 'Edgewise stiffness [Nm$^2$]'

nofpm_plot = nofpm_df['E'] * nofpm_df['I_y']

l1, = ax.plot(ed_df[ed_key], label='ElastoDyn', alpha=alpha)
l2, = ax.plot(nofpm_plot, label='H2-CNT', alpha=alpha)
ax.plot(bd_df[bd_key], c=l1.get_color(), linestyle='--', label='BeamDyn', alpha=alpha)
ax.plot(fpm_df[fpm_key], c=l2.get_color(), linestyle='--', label='H2-FPM', alpha=alpha)
ax.set_xlim([0, blade_len])
ax.grid('on')
ax.set_title(label)

# ========================================================
ax = axs[1, 0]  # torsional stiffness
bd_key, fpm_key, label = 'K_66', 'K_66', 'Torsional stiffness [Nm$^2$]'

ax.plot(bd_df[bd_key], linestyle='--', label='BeamDyn', alpha=alpha)
ax.plot(fpm_df[fpm_key], linestyle='--', label='H2-FPM', alpha=alpha)
ax.set_xlim([0, blade_len])
ax.grid('on')
ax.set_title(label)


# prettify and save
axs[0, 1].legend()
plt.tight_layout()
if save_fig:
    figname = os.path.basename(__file__).replace('.py', '.png')
    fig.savefig(fig_dir + figname, dpi=150)