import matplotlib
matplotlib.use('agg')
from tools.plot_Bscan import mpl_plot
import matplotlib.pyplot as plt
import os

import numpy as np


def save_img(filename, outputdata, dt, rxnumber, rxcomponent, out_dir):

    _, filename = os.path.split(filename)
    savefile = os.path.splitext(filename)[0]

    

    plt.axis('off')
    plt.imshow(
        outputdata,
        extent=[0,
                outputdata.shape[1],
                outputdata.shape[0] * dt,
                0],
        interpolation='nearest',
        aspect='auto',
        cmap='gray',
        vmin=-np.amax(np.abs(outputdata)),
        vmax=np.amax(np.abs(outputdata)))

    plt.savefig(out_dir + os.sep + savefile + '.png', format='png')


    outputdata = outputdata - np.mean(outputdata, axis=1, keepdims=True)
    outputdata = outputdata * (
            np.arange(outputdata.shape[0])/outputdata.shape[0]).reshape(outputdata.shape[0], 1)
    plt.imshow(
        outputdata,
        extent=[0,
                outputdata.shape[1],
                outputdata.shape[0] * dt,
                0],
        interpolation='nearest',
        aspect='auto',
        cmap='gray',
        vmin=-np.amax(np.abs(outputdata)),
        vmax=np.amax(np.abs(outputdata)))
    plt.savefig(out_dir + os.sep + savefile + '_pre' + '.png', format='png')
        
        
