# -*- coding: utf-8 -*-
"""Reused utilities in the scripts
"""
import subprocess
from _inputs import hawc2s_path


def run_hawc2s(path, cwd):
    """Run HAWC2S on a file"""
    out = subprocess.run([hawc2s_path, path], capture_output=True,
                         cwd=cwd)
    if out.returncode:
        raise ValueError(f'HAWC2S failed!!! Error output:\n\n'
                         + out.stderr.decode('UTF-8'))
