# -*- coding: utf-8 -*-
"""Reused file paths and parameters.

End all directory paths with slash!
"""


# file pathcs
hawc2s_path = 'C:/Users/rink/Documents/hawc2/hawcstab2_v2.16a_x64/HAWC2S_x64.exe'
hawc_dir = 'C:/Users/rink/git/IEA-15-240-RWT/HAWC2/'
res_dir = '../results/'
fig_dir = '../figures/'
steady_dir = res_dir + 'steady_v1/'
step_dir = res_dir + 'step_v1/'
dlc11_dir = res_dir + 'DLC11_v1/'
# parameters
model_keys = [('ED', 'NoFPM_notorsion'), ('BD', 'FPM')]
fast_labels = ['ElastoDyn', 'BeamDyn']
h2_labels = ['H2-PTNT', 'H2-FPM']
prebend = 4.0014  # prebend at tip of blade [m]
blade_len = 117.148749
# hawc2 input channels
i_gspd = 2
i_pit= 3
i_trq = 10
i_thr = 12
i_uhub = 14
i_tbfa = 19
i_tbss = 20
i_ywbr = 22
i_ywrl = 23
i_flp = 31
i_edg = 32
i_tipe = 44
i_tipf = 45
i_gtrq = 95
i_pow = 96
# stuff for plotting
plot_dict = {'BldPitch1': (i_pit, 'Blade pitch [deg]', 1),  # fast key, hawc2 channel, plot label, scale
             'GenSpeed': (i_gspd, 'Generator speed [rpm]', 1),
             'GenPwr': (i_pow, 'Power [MW]', 1e-3),
             'GenTq': (i_gtrq, 'Generator torque [MNm]', 1e-3),
             'RootMyb1': (i_flp, 'Flapwise root moment [MNm]', 1e-3),
             'RootMxb1': (i_edg, 'Edgewise root moment [MNm]', 1e-3),
             'TipDxb1': (i_tipf, 'Flapwise tip deflection [m]', 1),
             'TipDyb1': (i_tipe, 'Edgewise tip deflection [m]', 1),
             'RtAeroFxh': (i_thr, 'Thrust [MN]', 1e-6),
             'TwrBsMyt': (i_tbfa, 'Tower-base fore-aft [MNm]', 1e-3),
             'TwrBsMxt': (i_tbss, 'Tower-base side-side [MNm]', 1e-3),
             'YawBrMxp': (i_ywrl, 'Yaw-bearing roll moment [MNm]', 1e-3),
             'YawBrMyp': (i_ywbr, 'Yaw-bearing pitch moment [MNm]', 1e-3),
             'RtAeroCp': (500, 'Cp [-]', 1),
             'RtAeroCt': (600, 'Ct [-]', 1),
    }