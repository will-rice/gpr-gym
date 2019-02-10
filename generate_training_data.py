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

X = 1.0
Y = 1.0
Z = 0.1
CYLINDER_X=0.33
CYLINDER_Y=0.33


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

for i in tqdm(range(1)):
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
                        'time_window', 12e-9)

                    soil_peplinski = command(
                        'soil_peplinski', sand, clay, 2.0,
                        2.66, 0.001, 0.25, 'my_soil'
                    )
                    box = command(
                        'fractal_box', 0, 0, 0, 1,
                        0.75, 0.1, 1.5, 1, 1, 1, 50,
                        'my_soil', 'my_soil_box', seed)
                    
                    roughness = command(
                        'add_surface_roughness', 0, 0, 0.1,
                        0.1, 0.1, 0.1, 1.5, 1, 1, 0.065, 0.080,
                        'my_soil_box'
                    )

                    

                    if pipe_material is 'pvc':
                        pvc = command(
                            'material', 3, 0,
                            1, 0, 'pvc')
                        cylinder = command(
                            'cylinder', CYLINDER_X, 0.33, 0, CYLINDER_X,
                            0.33, Z, diameter, 'pvc', 'y')
                    elif pipe_material is 'pec':
                        cylinder = command(
                            'cylinder', CYLINDER_X, 0.33, 0, CYLINDER_X,
                            0.33, Z, diameter, 'pec', 'y')
                    else:
                        concrete =  pvc = command(
                            'material', 6, 0,
                            1, 0, 'concrete')
                        cylinder = command(
                            'cylinder', CYLINDER_X, 0.33, 0, CYLINDER_X,
                            0.33, Z, diameter, 'concrete', 'y')

                    rx = command(
                        'rx', 0.1125, 0.1525, 0)

                    src_steps = command(
                        'src_steps', 0.002, 0.0, 0)

                    rx_steps = command(
                        'rx_steps', 0.002, 0.0, 0)

                    waveform = command(
                        'waveform', 'ricker', 1,
                        900e6, 'my_ricker')

                    hertzian_dipole = command(
                        'hertzian_dipole', 'z', 0.150,
                        0.170, 0, 'my_ricker')

                    geometry_view = command(
                        'geometry_view', 0, 0,
                        0, X, Y, 0.002, 0.002,
                        0.002, 0.002, 'cylinder_half_space',
                        'n')

                    message = command('messages', 'n')

                    with open(
                        os.path.join(
                        'input-files',
                        'cylinder_Bscan_2D_{}_{}_{}_{}.in'.format(
                        i,
                        pipe_material,
                        np.round(diameter, decimals=4),
                        sand)), 'w') as f:
                        f.write(domain+'\n')
                        f.write(dx_dy_dz+'\n')
                        f.write(time_window+'\n')
                        f.write(soil_peplinski+'\n')
                        f.write(box+'\n')
                        f.write(roughness+'\n')

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
                        #f.write(geometry_view+'\n')
                        f.write(message)

Generator(n_scans=200, in_dir='input-files/*.in', out_dir='output-files/')