import os
import argparse
from glob import glob

import matplotlib.pyplot as plt

from gprMax.gprMax import api
from tools.outputfiles import merge_files
from tools.plot_Bscan import get_output_data

from utils import save_img


class Generator:
    def __init__(self, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.in_file_paths = glob(in_dir)
        self.rx_number = 1
        self.rx_component = 'Ez'

        for path in self.in_file_paths:
            self._create_ascan(path)
            self._merge_ascan(path)
            output_data, dt = self._prepare_bscan(path)
            save_img(
                path,
                output_data,
                dt,
                self.rx_number,
                self.rx_component,
                self.out_dir)

    def _create_ascan(self, path):
        api(path, n=60, geomerty_only=False)

    def _merge_ascan(self, path):
        filename, _ = os.path.splitext(path)
        merge_files(filename)

    def _prepare_bscan(self, path):
        filename, _ = os.path.splitext(path)
        filename = filename + '_merged.out'
        return get_output_data(
            filename,
            self.rx_number,
            self.rx_component)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--in_dir', help='name of the input directory')
    parser.add_argument(
        '--out_dir', help='name of output directory')
    args = parser.parse_args()

    Generator(args.out_dir, args.in_dir)
