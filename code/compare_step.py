# -*- coding: utf-8 -*-
"""Compare step-wind responses
"""
import matplotlib.pyplot as plt
import pandas as pd
from wetb.hawc2.Hawc2io import ReadHawc2
from _inputs import (step_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq)

def read_step(path):
    """Read a steady result"""
    if path.endswith('.out'):  # openfast result
        df = pd.read_csv(path, skiprows=[0,1,2,3,4,5] + [7], index_col=0, header=0,
                         delim_whitespace=True)
    elif path.endswith('.sel'):  # hawc2 result
        df = pd.DataFrame(ReadHawc2(path).ReadBinary()).set_index(0)
    else:
        raise ValueError('Path must end in out or sel!')
    return df


fast_path = step_dir + 'IEA15MW_step_torque_ED_0.out'
h2_path = step_dir + 'iea_15mw_rwt_NoFPM_notorsion_step.sel'

fast_df = read_step(fast_path)
h2_df = read_step(h2_path)

#%%

fig, axs = plt.subplots(1, 4, num=2, clear=True, figsize=(10, 3))

plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('GenPwr', i_pow, 1e-3),
             ('GenTq', i_gtrq, -1e-3)]


for j, (fast_key, h2_chan, h2scl) in enumerate(plot_keys):
    if 'RootM' in fast_key and 'BD' in fastname:
        fast_key = 'B1RootMyr'
        h2scl = -1e3

    ax = axs[j]

    fast_data = fast_df[fast_key]
    h2_data = h2_df[h2_chan] * h2scl

    ax.plot(fast_data, label='OF')
    ax.plot(h2_data, label='H2')
    ax.set_title(f'{fast_key}')
    ax.set_xlim([200, h2_data.index[-1]])

axs[0].legend()
plt.tight_layout()
