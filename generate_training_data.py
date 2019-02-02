import matplotlib
matplotlib.use('agg')

from generator import Generator
from tqdm import tqdm
import os
import numpy as np
from gprMax.input_cmd_funcs import command
import matplotlib.pyplot as plt



pipe_materials = ['pec', 'pvc']

diameters = np.arange(start=0.002,
                      stop=0.1,
                      step=0.002)


for i in range(10):

    for pipe_material in pipe_materials:

        for diameter in diameters:

            domain = command(
                'domain', 1, 1, 0.002)

            dx_dy_dz = command(
                'dx_dy_dz', 0.002, 0.002, 0.002)

            time_window = command(
                'time_window', 12e-9)

            material = command(
                'material', 3, 0.1,
                1.0, 0.0, 'saturated_sand')

            box = command(
                'box', 0.0, 0.0, 0.0, 1,
                0.8, 0.002, 'saturated_sand')

            if pipe_material is 'pvc':
                pvc = command(
                    'material', 3, 0,
                    1, 0, 'pvc')
                cylinder = command(
                    'cylinder', 0.33, 0.33, 0, 0.33,
                    0.33, 0.002, diameter, 'pvc', 'y')
            else:
                cylinder = command(
                    'cylinder', 0.33, 0.33, 0, 0.33,
                    0.33, 0.002, diameter, 'pec', 'y')

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
                0, 1.0, 1.0, 0.002, 0.002,
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

                f.write(box+'\n')
                f.write(cylinder+'\n')
                f.write(rx+'\n')
                f.write(src_steps+'\n')
                f.write(rx_steps+'\n')
                f.write(waveform+'\n')
                f.write(hertzian_dipole+'\n')
                f.write(geometry_view+'\n')
                f.write(message)

Generator('input-files/*.in', 'output-files')
