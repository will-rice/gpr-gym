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

X = 1
Y = 1


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


pipe_materials = ['pec', 'pvc', 'concrete']
ground_materials = ['sand', 'saturated_sand', 'dirt', 'clay', 'mixed']

diameters = np.arange(start=0.01,
                      stop=0.1,
                      step=0.01)

start = time.time()
for i in tqdm(range(10)):

    blockPrint()
    for pipe_material in pipe_materials:

        for ground in ground_materials:

            for diameter in diameters:

                domain = command(
                    'domain', X, Y, 0.002)

                dx_dy_dz = command(
                    'dx_dy_dz', 0.002, 0.002, 0.002)

                time_window = command(
                    'time_window', 12e-9)

                if ground is 'saturated_sand':
                    material = command(
                        'material', 20, 0.1,
                        1.0, 0.0, 'ground')
                    box = command(
                    'box', 0.0, 0.0, 0.0, X,
                    Y*.75, 0.002, 'ground')
                elif ground is 'dirt':
                    material = command(
                        'material', 5, 0.1,
                        1.0, 0.0, 'ground')
                    box = command(
                        'box', 0.0, 0.0, 0.0, X,
                    Y*.75, 0.002, 'ground')
                elif ground is 'clay':
                    material = command(
                        'material', 10, 0.1,
                        1.0, 0.0, 'ground')
                    box = command(
                    'box', 0.0, 0.0, 0.0, X,
                    Y*.75, 0.002, 'ground')
                elif ground is 'sand':
                    material = command(
                        'material', 3, 0.01,
                        1.0, 0.0, 'ground')
                    box = command(
                    'box', 0.0, 0.0, 0.0, X,
                    Y*.75, 0.002, 'ground')
                else:
                    sat_sand = command(
                        'material', 20, 0.1,
                        1.0, 0.0, 'saturated_sand')
                    dirt = command(
                        'material', 5, 0.1,
                        1.0, 0.0, 'dirt')
                    clay = command(
                        'material', 10, 0.1,
                        1.0, 0.0, 'clay')
                    sand = command(
                        'material', 3, 0.01,
                        1.0, 0.0, 'sand')
                    box = command(
                    'box', 0.0, 0.0, 0.0, X,
                    Y*.75, 0.002, 'saturated_sand')
                     
                

                if pipe_material is 'pvc':
                    pvc = command(
                        'material', 3, 0,
                        1, 0, 'pvc')
                    cylinder = command(
                        'cylinder', 0.33, 0.33, 0, 0.33,
                        0.33, 0.002, diameter, 'pvc', 'y')
                elif pipe_material is 'pec':
                    cylinder = command(
                        'cylinder', 0.33, 0.33, 0, 0.33,
                        0.33, 0.002, diameter, 'pec', 'y')
                else:
                    concrete =  pvc = command(
                        'material', 9, 0,
                        0.01, 0, 'concrete')
                    cylinder = command(
                        'cylinder', 0.33, 0.33, 0, 0.33,
                        0.33, 0.002, diameter, 'concrete', 'y')

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
                        'cylinder_Bscan_2D_{}_{}_{}.in'.format(
                            i,
                            pipe_material,
                            np.round(diameter, decimals=4))), 'w') as f:
                    f.write(domain+'\n')
                    f.write(dx_dy_dz+'\n')
                    f.write(time_window+'\n')
                    f.write(material+'\n')

                    if pipe_material is 'pvc':
                        f.write(pvc+'\n')
                    elif pipe_material is 'concrete':
                        f.write(concrete+'\n')
                    else:
                        pass

                    if ground is 'mixed':
                        f.write(sat_sand+'\n')
                        f.write(dirt+'\n')
                        f.write(clay+'\n')
                        f.write(sand+'\n')
                        f.write(box+' dirt' + ' clay'+'\n')
                    else:
                        f.write(box+'\n')

                    f.write(cylinder+'\n')
                    f.write(rx+'\n')
                    f.write(src_steps+'\n')
                    f.write(rx_steps+'\n')
                    f.write(waveform+'\n')
                    f.write(hertzian_dipole+'\n')
                    #f.write(geometry_view+'\n')
                    f.write(message)

Generator('input-files/*.in', 'output-files')
end = time.time()
with open('time.txt', 'w') as f:
    f.write((end-start))