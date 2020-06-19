# -*- coding: utf-8 -*-
"""Convert hdf5 to csv for sharing
"""
from _inputs import res_dir
import pandas as pd


h5_path = res_dir + 'DLC11_v1/NoFPM_notorsion_DLC11_statistics.h5'  # NoFPM_notorsion = TNT
csv_path = res_dir + 'DLC11_v1/DLC11_TNT_statistics.csv'


df = pd.read_hdf(h5_path, 'table')
df.to_csv(csv_path)
