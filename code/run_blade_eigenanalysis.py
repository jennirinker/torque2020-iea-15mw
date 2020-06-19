# -*- coding: utf-8 -*-
"""Use HAWC2S to calculate blade eigenanalysis
"""
import os
from wetb.hawc2.htc_file import HTCFile
from _inputs import hawc_dir, data_dir
from _utils import run_hawc2s


for h2_mod in ['FPM', 'NoFPM_notorsion']:

    # intermediate variables
    mod_dir = hawc_dir + h2_mod + '/'

    # create hawc2s file for blade eigenanalysis
    orig_htc = os.path.join(mod_dir, [f for f in os.listdir(mod_dir)
                                      if f.endswith('.htc')][0])
    new_htc = mod_dir + f'{h2_mod}_blade_eigenanalysis.htc'
    htc = HTCFile(orig_htc)
    htc.hawcstab2.add_line('compute_structural_modal_analysis', ['bladeonly', 20])
    htc.save(new_htc)

    # run hawc2s
    run_hawc2s(new_htc, mod_dir)
    cmb_path = new_htc.replace('.htc', '_Blade_struc.cmb')

    # move results to data directory
    os.replace(cmb_path, data_dir + f'eigenfreq_{h2_mod}_hawc2.txt')

    # delete hawc2s file
    os.remove(new_htc)
