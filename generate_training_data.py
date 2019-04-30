import matplotlib
matplotlib.use('agg')

from generator import Generator
from tqdm import tqdm
import os
import sys
import numpy as np
import time
from gprMax.input_cmd_funcs import command
import matplotlib.pyplot as plt

X = 0.5
Y = 0.5
Z = 0.002
CYLINDER_X=0.15
CYLINDER_Y=0.080


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


pipe_materials = ['pec', 'pvc', 'concrete']
# ground materials are what the primary component of peplinksi mixture is

sand_fraction = np.arange(start=0.1,
                          stop=0.9,
                          step=0.1)
clay_fraction = np.arange(start=0.1,
                          stop=0.9,
                          step=0.1)

diameters = np.arange(start=0.01,
                      stop=0.1,
                      step=0.01)

for i in tqdm(range(20)):
    seed = np.random.randint(1)

    blockPrint()
    for pipe_material in pipe_materials:

        for sand in sand_fraction:

            for clay in reversed(clay_fraction):

                for diameter in diameters:

                    domain = command(
                        'domain', X, Y, Z)

                    dx_dy_dz = command(
                        'dx_dy_dz', 0.002, 0.002, 0.002)

                    time_window = command(
                        'time_window', 5e-9)

                    soil_peplinski = command(
                        'soil_peplinski', sand, clay, 2.0,
                        2.66, 0.001, 0.25, 'my_soil'
                    )
                    box = command(
                        'fractal_box', 0, 0, 0, X,
                        0.75 * Y, Z, 1.5, 1, 1, 1, 50,
                        'my_soil', 'my_soil_box', seed)
                   

                    

                    if pipe_material is 'pvc':
                        pvc = command(
                            'material', 3, 0,
                            1, 0, 'pvc')
                        cylinder = command(
                            'cylinder', CYLINDER_X, CYLINDER_Y, 0, CYLINDER_X,
                            CYLINDER_Y, Z, diameter, 'pvc', 'y')
                    elif pipe_material is 'pec':
                        cylinder = command(
                            'cylinder', CYLINDER_X, CYLINDER_Y, 0, CYLINDER_X,
                            CYLINDER_Y, Z, diameter, 'pec', 'y')
                    else:
                        concrete =  pvc = command(
                            'material', 6, 0,
                            1, 0, 'concrete')
                        cylinder = command(
                            'cylinder', CYLINDER_X, CYLINDER_Y, 0, CYLINDER_X,
                            CYLINDER_Y, Z, diameter, 'concrete', 'y')

                    rx = command(
                        'rx', 0.080, 0.170, 0)

                    src_steps = command(
                        'src_steps', 0.002, 0.0, 0)

                    rx_steps = command(
                        'rx_steps', 0.002, 0.0, 0)

                    waveform = command(
                        'waveform', 'ricker', 1,
                        1.5e9, 'my_ricker')

                    hertzian_dipole = command(
                        'hertzian_dipole', 'z', 0.040,
                        0.170, 0, 'my_ricker')

                    message = command('messages', 'n')

                    with open(os.path.join('input-files',
                                           'cylinder_Bscan_2D_{}_{}_{}_{}.in'.format(
                        i,
                        pipe_material,
                        np.round(diameter, decimals=4),
                        np.round(sand, decimals=4))), 'w') as f:
                        f.write(domain+'\n')
                        f.write(dx_dy_dz+'\n')
                        f.write(time_window+'\n')
                        f.write(soil_peplinski+'\n')
                        f.write(box+'\n')

                        if pipe_material is 'pvc':
                            f.write(pvc+'\n')
                        elif pipe_material is 'concrete':
                            f.write(concrete+'\n')
                        else:
                            pass
                        
                        f.write(cylinder+'\n')
                        f.write(rx+'\n')
                        f.write(src_steps+'\n')
                        f.write(rx_steps+'\n')
                        f.write(waveform+'\n')
                        f.write(hertzian_dipole+'\n')
                        f.write(message)

Generator(n_scans=100, in_dir='input-files/*.in', out_dir='output-files/')