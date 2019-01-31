import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from gprMax.input_cmd_funcs import command
import numpy as np
import os
from generator import Generator



dx_values = np.arange(start=0.25,
                      stop=1.0,
                      step=0.05)
diameters = np.arange(start=0.25,
                      stop=1.0,
                      step=0.05)

for value in dx_values: 
    for diameter in diameters:
        domain = command('domain', 2.5, 2.5, 0.002)
        dx_dy_dz = command('dx_dy_dz', 0.002, 0.002, 0.002)
        time_window = command('time_window', 12e-9)
        material = command('material', 20.0, 0.1, 1.0, 0.0, 'saturated_sand')
        box = command('box', 0.0, 0.0, 0, 2.5, 0.15, 0.0025, 'saturated_sand')
        cylinder = command('cylinder',
                           value,
                           0.08,
                           0,
                           value,
                           0.08,
                           0.002,
                           diameter,
                           'pec',
                           'y')
        rx = command('rx', 0.1125, 0.1525, 0)
        src_steps = command('src_steps', 0.002, 0.0, 0)
        rx_steps = command('rx_steps', 0.002, 0.0, 0)
        waveform = command('waveform', 'ricker', 1, 900e6, 'my_ricker')
        hertzian_dipole = command('hertzian_dipole', 'z', 0.150, 0.170, 0, 'my_ricker')

        with open(
            os.path.join(
                'input-files',
                'cylinder_Bscan_2D_{}_{}.in'.format(str(np.round(value, 1)), np.round(diameter))), 'w') as f:
            f.write(domain+'\n')
            f.write(dx_dy_dz+'\n')
            f.write(time_window+'\n')
            f.write(material+'\n')
            f.write(box+'\n')
            f.write(cylinder+'\n')
            f.write(rx+'\n')
            f.write(rx_steps+'\n')
            f.write(waveform+'\n')
            f.write(hertzian_dipole)



Generator('input-files/*.in', 'output-files')