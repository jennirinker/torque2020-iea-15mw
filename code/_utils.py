# -*- coding: utf-8 -*-
"""Reused utilities in the scripts
"""
import subprocess
import numpy as np
import pandas as pd
from wetb.hawc2.Hawc2io import ReadHawc2
import yaml
from _inputs import hawc2s_path


def run_hawc2s(path, cwd):
    """Run HAWC2S on a file"""
    out = subprocess.run([hawc2s_path, path], capture_output=True,
                         cwd=cwd)
    if out.returncode:
        raise ValueError(f'HAWC2S failed!!! Error output:\n\n'
                         + out.stderr.decode('UTF-8'))


def read_blade_dat(path, n_ed=50, blade_len=117.148749):
    """Read blade dat file"""

    def read_beamdyn(path, blade_len=blade_len):
        m_cols = [f'M_{i}{j}' for i in range(1,7) for j in range(i,7)]
        k_cols = [f'K_{i}{j}' for i in range(1,7) for j in range(i,7)]
        bd_cols = ['r'] + m_cols + k_cols
        with open(path, 'r') as f:
            for i, line in enumerate(f):
                if i == 3:
                    nstats = int(line.split()[0])  # number of stations
                    bd_stat = []
                if not (i - 10) % 15:
                    bd_stat.append(float(line))
        bd_df = pd.DataFrame(columns=bd_cols)
        bd_df['r'] =  np.array(bd_stat) * blade_len
        for i in range(nstats):
            mi = np.loadtxt(path, skiprows=15*i+18, max_rows=6)
            ki = np.loadtxt(path, skiprows=15*i+11, max_rows=6)
            bd_df.loc[i, m_cols] = mi[np.triu_indices(6)]
            bd_df.loc[i, k_cols] = ki[np.triu_indices(6)]
        return bd_df.set_index('r')

    def read_elastodyn(path, n_ed=n_ed, blade_len=blade_len):
        ed_df = pd.read_csv(path, delim_whitespace=True, skiprows=list(range(14)) + [15],
                            nrows=n_ed, header=0)
        ed_df.iloc[:, 0] = ed_df.iloc[:, 0] * blade_len
        return ed_df.set_index('BlFract')

    def read_hawc2(path):
        nofpm_cols = ['r', 'm', 'x_cg', 'y_cg', 'ri_x', 'ri_y', 'x_sh', 'y_sh', 'E', 'G', 'I_x',
              'I_y', 'K', 'k_x', 'k_y', 'A', 'pitch', 'x_e', 'y_e']
        fpm_cols = ['r', 'm', 'x_cg', 'y_cg', 'ri_x', 'ri_y', 'pitch', 'x_e', 'y_e', 'K_11',
                    'K_12', 'K_13', 'K_14', 'K_15', 'K_16', 'K_22', 'K_23', 'K_24', 'K_25',
                    'K_26', 'K_33', 'K_34', 'K_35', 'K_36', 'K_44', 'K_45', 'K_46', 'K_55',
                    'K_56', 'K_66']
        with open(path, 'r') as f:
            for i, line in enumerate(f):
                if line.startswith('$'):
                    max_rows = int(line.split()[1])
                    skiprows = i + 1
                    break
        h2_dat = np.loadtxt(path, skiprows=skiprows, max_rows=max_rows)
        h2_df = pd.DataFrame(h2_dat, columns=[nofpm_cols, fpm_cols][h2_dat.shape[1] == 30])
        return h2_df.set_index('r')

    if 'BeamDyn_blade' in path:
        return read_beamdyn(path, blade_len=blade_len)
    elif 'ElastoDyn_blade' in path:
        return read_elastodyn(path, n_ed=n_ed, blade_len=blade_len)
    elif 'Blade_st' in path:
        return read_hawc2(path)
    else:
        return ValueError('Unrecognized path ' + path + '!!!')


def read_dlc11(path):
    """Read the DLC11 results"""
    if path.endswith('yaml'):
        with open(path) as f:
            df = pd.DataFrame.from_dict(yaml.load(f, Loader=yaml.FullLoader))
    elif path.endswith('h5'):
        df = pd.read_hdf(path, 'table')
    else:
        raise ValueError('Path must beh5 or yaml!!!')
    return df


def read_eigenfreq(path, nread=13):
    """Read an eigenfrequency result, return array"""
    if path.endswith('openfast.txt') and '_BD_' in path:
        all_freqs =  np.loadtxt(path, skiprows=1)
        return np.mean(all_freqs.reshape(-1, 3), axis=1)[:nread]
    elif path.endswith('openfast.txt') and '_ED_' in path:
        return np.loadtxt(path, skiprows=1)[:nread]
    elif path.endswith('hawc2.txt'):
        return np.loadtxt(path, skiprows=1)[1:nread+1]
        
    else:
        raise ValueError('Filename must end with openfast.txt or hawc2.txt!')


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


def read_step(path, usecols=None):
    """Read a stepwind result"""
    if usecols is not None:
        usecols = ['Time', 'Wind1VelX'] + usecols
    if path.endswith('.out'):  # openfast result
        df = pd.read_csv(path, skiprows=[0,1,2,3,4,5] + [7], index_col=0, header=0,
                         delim_whitespace=True, usecols=usecols)
    elif path.endswith('.sel'):  # hawc2 result
        df = pd.DataFrame(ReadHawc2(path).ReadBinary()).set_index(0)
    else:
        raise ValueError('Path must end in out or sel!')
    return df