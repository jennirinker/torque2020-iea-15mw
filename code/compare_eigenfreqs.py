# -*- coding: utf-8 -*-
"""Create table of eigenfrequencies
"""
import numpy as np
from _inputs import data_dir, model_keys
from _utils import read_eigenfreq


tab_path = data_dir + 'eigendata.tab'
model_keys = [model_keys[0]]  # don't have elastodyn yet
nread = 8  # number of frequencies to look at

data = np.empty((nread, len(model_keys)*3))
for i, (fkey, h2key) in enumerate(model_keys):
    # load the frequencies
    fast_path = data_dir + f'eigenfreq_{fkey}_openfast.txt'
    hawc2_path = data_dir + f'eigenfreq_{h2key}_hawc2.txt'
    data[:, 3*i] = read_eigenfreq(fast_path, nread=nread)
    data[:, 3*i+1] = read_eigenfreq(hawc2_path, nread=nread)
    data[:, 3*i+2] = (data[:, 3*i] - data[:, 3*i+1])/(data[:, 3*i] + data[:, 3*i+1])*200

with open(tab_path, 'w') as f:
    f.write('  & ' +  ' & '.join(f'{tup[0]} & {tup[1]} & PercDiff'
                                 for tup in model_keys)
            + ' \\\\\n')
    for i in range(nread):
        f.write(f' {i+1} & ' + ' & '.join(f'{x:.3f}' for x in data[i]) + ' \\\\\n')


