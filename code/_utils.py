# -*- coding: utf-8 -*-
"""Reused utilities in the scripts
"""
import subprocess
import numpy as np
from _inputs import hawc2s_path


def run_hawc2s(path, cwd):
    """Run HAWC2S on a file"""
    out = subprocess.run([hawc2s_path, path], capture_output=True,
                         cwd=cwd)
    if out.returncode:
        raise ValueError(f'HAWC2S failed!!! Error output:\n\n'
                         + out.stderr.decode('UTF-8'))


def read_eigenfreq(path, nread=13):
    """Read an eigenfrequency result, return array"""
    if path.endswith('openfast.txt'):
        all_freqs =  np.loadtxt(path, skiprows=1)
        return np.mean(all_freqs.reshape(-1, 3), axis=1)[:nread]
    elif path.endswith('hawc2.txt'):
        return np.loadtxt(path, skiprows=1)[1:nread+1]
        
    else:
        raise ValueError('Filename must end with openfast.txt or hawc2.txt!')