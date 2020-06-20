# -*- coding: utf-8 -*-
"""compare steady states
"""
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from _inputs import (steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow, i_flp,
                     i_tbfa, i_gtrq)

def read_steady(path):
    """Read a steady result"""
    if path.endswith('.yaml'):  # nrel result
        with open(path) as f:
            df = pd.DataFrame.from_dict(yaml.load(f, Loader=yaml.FullLoader))
    elif path.endswith('csv'):  # dtu result
        df = pd.read_csv(path, index_col=[0,1]).swaplevel(0, 1)
    else:
        raise ValueError('Must end in yaml or csv!')
    return df


plot_keys = [('BldPitch1', i_pit, 1), ('GenSpeed', i_gspd, 1), ('GenPwr', i_pow, 1e-3),
             ('GenTq', i_gtrq, -1e-3), ('RootMyb1', i_flp, -1), ('TwrBsMyt', i_tbfa, 1)]

# can plot up to 8
fig, axs = plt.subplots(4, 4, figsize=(12, 8), clear=True, num=1)

for i, (fastname, h2name) in enumerate(model_keys):
    # make paths
    h2_path = steady_dir + f'{h2name}_Steady_stats.csv'
    fast_path = steady_dir + f'IEA15MW_torque_steady_{fastname}_stats.yaml' 
    h2_nofpm = steady_dir + f'NoFPM_Steady_stats.csv'

    # load data
    h2_df = read_steady(h2_path)
    fast_df = read_steady(fast_path)
    nofpm_df = read_steady(h2_path)
    for j, (fast_key, h2_chan, h2scl) in enumerate(plot_keys):
        if 'RootM' in fast_key and 'BD' in fastname:
            fast_key = 'B1RootMyr'
            h2scl = -1e3
    
        ax = axs[2*(j//4) + i, j % 4]

        fast_wsp, fast_data = fast_df.loc['mean', ['Wind1VelX', fast_key]]
        h2_wsp, h2_data = h2_df.loc['mean'][[str(i_uhub), str(h2_chan)]].values.T
        nofpm_wsp, nofpm_data = nofpm_df.loc['mean'][[str(i_uhub),
                                                      str(h2_chan)]].values.T

        h2_data *= h2scl
        nofpm_data *= h2scl

        ax.plot(h2_wsp, h2_data, label='H2')
        ax.plot(fast_wsp, fast_data, label='OF')
        ax.set_title(f'{fast_key},\n {h2name} vs. {fastname}')

        if i == 1:
            ax.plot(nofpm_wsp, nofpm_data, label='H2 nofpm')

    
axs[1, 1].legend()
plt.tight_layout()