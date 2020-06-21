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
        usecols = ['Time'] + usecols
    if path.endswith('.out'):  # openfast result
        df = pd.read_csv(path, skiprows=[0,1,2,3,4,5] + [7], index_col=0, header=0,
                         delim_whitespace=True, usecols=usecols)
    elif path.endswith('.sel'):  # hawc2 result
        df = pd.DataFrame(ReadHawc2(path).ReadBinary()).set_index(0)
    else:
        raise ValueError('Path must end in out or sel!')
    return df