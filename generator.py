import matplotlib
matplotlib.use('agg')

import os
import argparse
from glob import glob

import numpy as np
from tqdm import tqdm

from gprMax.gprMax import api
from tools.outputfiles_merge import merge_files
from tools.plot_Bscan import get_output_data

from utils import save_img


class Generator:
    def __init__(self, n_scans, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.in_file_paths = glob(in_dir)
        self.in_file_paths.sort()
        self.rx_number = 1
        self.rx_component = 'Ez'
        self.n_scans = n_scans

        for path in tqdm(self.in_file_paths):
            self._create_ascan(path)
            self._merge_ascan(path)
            outputdata, dt = self._prepare_bscan(path)
            save_img(path,
                     outputdata,
                     dt,
                     self.rx_number,
                     self.rx_component,
                     self.out_dir)

    def _create_ascan(self, path):
        api(path,
            n=self.n_scans,
            geometry_only=False,
            gpu=[0])

    def _merge_ascan(self, path):
        filename, _ = os.path.splitext(path)
        merge_files(filename, removefiles=True)

    def _prepare_bscan(self, path):
        filename, _ = os.path.splitext(path)
        filename = filename + '_merged.out'
        return get_output_data(filename,
                               self.rx_number,
                               self.rx_component)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--in_dir', help='name of the input directory')
    parser.add_argument(
        '--out_dir', help='name of output directory')
    args = parser.parse_args()

    Generator(200, args.out_dir, args.in_dir)
