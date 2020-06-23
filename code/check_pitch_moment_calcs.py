# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:46:51 2020

@author: rink
"""
import numpy as np

                # mass          # downwind dist
iner = np.array([[0.9548E+06,  0.0000E+00],  # tower
                [0.6309E+06, -0.3945E+01],  # towertop [yaw sys + nac mass]
                [0.5968E+01, -0.2967E+01],  # connector
                [0.1900E+06, -0.1107E+02],  # shaft [hub mass]
                [0.3000E+01, -0.1102E+02],  # hub1
                [0.3000E+01, -0.1126E+02],  # hub2
                [0.3000E+01, -0.1126E+02],  # hub3
                [0.6361E+05, -0.9983E+01],  # blade1
                [0.6361E+05, -0.1473E+02],  # blade2
                [0.6361E+05, -0.1467E+02]  # blade3
                ])

yaw_sys = 1.000e+05  # remove this
h2_mom = -np.product(iner, axis=1).sum() / 1e3  # kNm
h2_mass = iner[1:].sum() - yaw_sys  # kg

hubmass = 190000
bmass = 62250
nacmass = 530888
hcent = 11.075
nacxcm = 4.688
nrel_mass = hubmass + nacmass + 3*bmass
nrel_mom = (hcent * (hubmass + 3*bmass) + nacmass*nacxcm) / 1e3  # kNm

print(f'H2 mass:           {h2_mass:.0f} kg')
print(f'OF mass:           {nrel_mass:.0f} kg')
print()
print(f'H2 yaw pitch mmnt: {h2_mom:.0f} kNm')
print(f'OF yaw pitch mmnt: {nrel_mom:.0f} kNm')

perc_diff = (h2_mom - nrel_mom) / nrel_mom * 100
print(f'H2 is higher than OF by {(h2_mom-nrel_mom):.0f} kNm ({perc_diff:.0f}%)')
