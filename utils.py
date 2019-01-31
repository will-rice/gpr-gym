import os

import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def save_img(filename, outputdata, dt, rxnumber, rxcomponent, out_dir):

    _, filename = os.path.split(filename)

    plt.imshow(outputdata,
               extent=[0, outputdata.shape[1], outputdata.shape[0] * dt, 0],
               interpolation='nearest',
               aspect='auto',
               cmap='gray',
               vmin=-np.amax(np.abs(outputdata)),
               vmax=np.amax(np.abs(outputdata)))

    plt.axis('off')

    savefile = os.path.splitext(filename)[0]
    plt.savefig(out_dir + savefile + '.png', format='png')
