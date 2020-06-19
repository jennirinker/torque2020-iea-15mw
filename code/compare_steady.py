# -*- coding: utf-8 -*-
"""compare steady states
"""
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from _inputs import steady_dir, model_keys, i_gspd, i_pit, i_uhub, i_pow

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


plot_keys = [('BldPitch1', i_pit), ('GenSpeed', i_gspd), ('GenPwr', i_pow)]


fig, axs = plt.subplots(2, len(plot_keys), figsize=(9, 4), clear=True, num=1)

for i, (fastname, h2name) in enumerate(model_keys):
    # load data
    h2_path = steady_dir + f'{h2name}_Steady_stats.csv'
    fast_path = steady_dir + f'IEA15MW_torque_steady_{fastname}_stats.yaml' 
    for j, (fast_key, h2_chan) in enumerate(plot_keys):
    
        ax = axs[i, j]
    
        h2_df = read_steady(h2_path)
        fast_df = read_steady(fast_path)

        fast_wsp, fast_data = fast_df.loc['mean', ['Wind1VelX', fast_key]]
        h2_wsp, h2_data = h2_df.loc['mean'][[str(i_uhub), str(h2_chan)]].values.T

        if 'GenPwr' in fast_key:  # units for generated power
            h2_data *= 1e-3

        ax.plot(h2_wsp, h2_data, label='H2')
        ax.plot(fast_wsp, fast_data, label='OF')
        ax.set_title(f'{fast_key},\n {h2name} vs. {fastname}')
axs[0, 1].legend()
plt.tight_layout()