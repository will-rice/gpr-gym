from scipy import signal
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')


def save_img(filename, outputdata, dt, rxnumber, rxcomponent, out_dir):

    _, filename = os.path.split(filename)
    savefile = os.path.splitext(filename)[0]

    plt.axis('off')
    plt.imsave(fname=out_dir + os.sep + savefile + '.png',
               arr=outputdata, cmap='gray',
               vmin=-np.amax(np.abs(outputdata)),
               vmax=np.amax(np.abs(outputdata)))

    plt.clf()

    fig = frequency_bscan(outputdata)
    plt.imsave(out_dir + os.sep + savefile + '_frequency' + '.png',
               fig, format='png',)
    plt.clf()

    outputdata = outputdata - np.mean(outputdata, axis=1, keepdims=True)
    outputdata = outputdata * (
        np.arange(outputdata.shape[0])/outputdata.shape[0]).reshape(outputdata.shape[0], 1)

    plt.axis('off')
    # plt.box(None)
    plt.imsave(out_dir + os.sep + savefile + '_post' + '.png',
               outputdata, cmap='gray',
               vmin=-np.amax(np.abs(outputdata)),
               vmax=np.amax(np.abs(outputdata)))

    # plt.savefig(out_dir + os.sep + savefile + '_post' + '.png',
    #           format='png', transparent=True,
    #          facecolor=None, pad_inches=0)
    plt.clf()

    fig = frequency_bscan(outputdata)
    plt.imsave(out_dir + os.sep + savefile + '_frequency_post' + '.png',
               fig, format='png')
    plt.clf()
    plt.close()


def frequency_bscan(outputdata):
    """ Frequency Distirbution of a B-scan """
    spects = []
    freqs = []
    times = []

    for i in range(len(outputdata[0, :])):
        f, t, zxx = stft(outputdata, i)
        freqs.append(f)
        times.append(t)
        spects.append(np.abs(zxx))

    spects = np.array(spects)
    freqs = np.array(freqs)
    times = np.array(times)
    spects = np.amax(spects, axis=1)

    # plt.grid(None)
    # plt.box(None)
    # plt.figure(figsize=(10,5))
    #plt.xlim(0, len(spects[:,0]))
    #plt.ylim(len(spects[0,:]), 0)
    # plt.pcolormesh(spects.transpose())
    # plt.set_cmap('viridis')
    # plt.tight_layout()
    # plt.axis('off')

    return spects.transpose()


def stft(inputs, index):
    """ Short Term Fourier Transform """
    f, t, zxx = signal.stft(inputs[:, index],
                            window='hann',
                            nperseg=4,
                            nfft=2048,
                            padded=None,
                            boundary=None)
    return f, t, zxx
