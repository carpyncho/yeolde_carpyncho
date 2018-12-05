
# coding: utf-8

#
# # Analisis de datos del tile b278

# ## Imports and global configurations

# In[51]:

from __future__ import print_function, division

import os
import warnings
import time
import argparse
import sys
import multiprocessing as mp

import numpy as np

import pandas as pd

import pytff

import tables as tb

from libs import mptables as mpt


# =============================================================================
# SUPRESS WARNINGS
# =============================================================================

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


# =============================================================================
# SA
# =============================================================================

class FourierDescriptor(tb.IsDescription):
    vvv_id = tb.Int64Col(pos=0)
    period = tb.FloatCol(pos=1)
    epoch = tb.FloatCol(pos=2)
    average_magnitude = tb.FloatCol(pos=3)
    N_data_point = tb.FloatCol(pos=4)
    sigma_obs_fit = tb.FloatCol(pos=5)
    A_1 = tb.FloatCol(pos=6)
    phi_1 = tb.FloatCol(pos=7)
    A_2 = tb.FloatCol(pos=8)
    phi_2 = tb.FloatCol(pos=9)
    A_3 = tb.FloatCol(pos=10)
    phi_3 = tb.FloatCol(pos=11)
    A_4 = tb.FloatCol(pos=12)
    phi_4 = tb.FloatCol(pos=13)
    A_5 = tb.FloatCol(pos=14)
    phi_5 = tb.FloatCol(pos=15)
    A_6 = tb.FloatCol(pos=16)
    phi_6 = tb.FloatCol(pos=17)
    A_7 = tb.FloatCol(pos=18)
    phi_7 = tb.FloatCol(pos=19)
    A_8 = tb.FloatCol(pos=20)
    phi_8 = tb.FloatCol(pos=21)
    A_9 = tb.FloatCol(pos=22)
    phi_9 = tb.FloatCol(pos=23)
    A_10 = tb.FloatCol(pos=24)
    phi_10 = tb.FloatCol(pos=25)
    A_11 = tb.FloatCol(pos=26)
    phi_11 = tb.FloatCol(pos=27)
    A_12 = tb.FloatCol(pos=28)
    phi_12 = tb.FloatCol(pos=29)
    A_13 = tb.FloatCol(pos=30)
    phi_13 = tb.FloatCol(pos=31)
    A_14 = tb.FloatCol(pos=32)
    phi_14 = tb.FloatCol(pos=33)
    A_15 = tb.FloatCol(pos=34)
    phi_15 = tb.FloatCol(pos=35)


# =============================================================================
# PROCESS
# =============================================================================

class ExtractFourier(mp.Process):

    def __init__(self, vvv_ids, sources_path, periods_path, rh5, procno):
        super(ExtractFourier, self).__init__()
        self.vvv_ids = vvv_ids
        self.sources_path = sources_path
        self.periods_path = periods_path
        self.rh5 = rh5
        self.chunk_size = 100
        self.procno = procno

    def get_obs(self, vvv_ids, obs_table):
        times, values = [], []
        for vvv_id in vvv_ids:
            query, data = "source_id == " + str(int(vvv_id)), []
            for r in obs_table.where(query):
                data.append({k: r[k] for k in obs_table.colnames})
            obs = pd.DataFrame(data)[obs_table.colnames]
            obs = obs.sort_values("hjd")
            times.append(obs.hjd.values)
            values.append(obs.mag.values)
        return pytff.stack_targets(times, values)

    def get_periods(self, vvv_ids, periods_table):
        periods = []
        for vvv_id in vvv_ids:
            query = "vvv_id == " + str(int(vvv_id))
            for r in periods_table.where(query):
                period = r["best_period"]
                periods.append(period)
        return np.array(periods)


    def dff_to_rows(self, dff, vvv_ids, columns):
        rows = []
        for idx, row in dff.iterrows():
            row = tuple([vvv_ids[idx]] + [row[k] for k in columns])
            rows.append(row)
        return rows

    def go(self, observations_table, periods_table):

        def sort_columns_key(coldata):
            return coldata[1]._v_pos

        columns = [
            k for k, _ in
            sorted(FourierDescriptor.columns.items(), key=sort_columns_key)
            if k != "vvv_id"]

        chunks = int(len(self.vvv_ids) / self.chunk_size)

        fourier = self.rh5.get_node("/fourier")
        for chunk_idx, vvv_ids in chunk_it(self.vvv_ids, chunks):

            tff = pytff.TFFCommand()
            print("[Storing '{}/p{}' ({})...]".format(chunk_idx, self.procno, tff.wrk_path))

            periods = self.get_periods(vvv_ids, periods_table)
            times, values = self.get_obs(vvv_ids, observations_table)

            tff_data, dff_data, match_data = tff.analyze(
                periods, times, values)

            dff = pd.DataFrame(dff_data)
            rows = self.dff_to_rows(dff, vvv_ids, columns)

            fourier.append(rows)
            fourier.flush()

    def run(self):
        with tb.open_file(self.sources_path) as obs_file, \
             tb.open_file(self.periods_path) as per_file:
                observations = obs_file.get_node("/observations")
                periods = per_file.get_node("/periods")
                self.go(observations, periods)


# =============================================================================
# RUND
# =============================================================================

def clean(vvv_ids, out_path):
    try:
        fourier = pd.read_hdf(out_path, 'fourier')
    except (IOError, KeyError):
        pass
    else:
        used =fourier.vvv_id.values
        if len(used):
            ids_filter = np.in1d(vvv_ids, used)
            vvv_ids = vvv_ids[~ids_filter]
    return vvv_ids


def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return enumerate(out)


def parse(argv):
    parser = argparse.ArgumentParser(description='Extract fourier components')
    parser.add_argument(
        '--sources', dest="sources", required=True,
        metavar='PATH', type=os.path.abspath,
        help='an h5 file dump from carpyncho')
    parser.add_argument(
        '--periods', dest="periods", metavar='PATH', required=True,
        type=os.path.abspath, help='an h5 file of periods')
    parser.add_argument(
        '--out', dest="out", metavar="PATH",
        type=os.path.abspath, required=True, help='h5 file to write into')
    parser.add_argument(
        '-p', "--procs", dest="procs", default=1,
        help="Number of process to span")
    return parser.parse_args(argv)


def main():
    args = parse(sys.argv[1:])

    print("[INFO] Retrieving sources...")
    sources = pd.read_hdf(args.sources, 'sources')
    sources = sources[sources["obs_number"] >= 30]
    sources = sources.id.values
    sources = clean(sources, args.out)
    print("[INFO] Found:", len(sources), "sources")

    print("[INFO] Chunk in", args.procs, "process")
    chunks = chunk_it(sources, args.procs)

    with tb.open_file(args.out, mode="a") as h5file:
        if "/fourier" not in h5file:
            fourier = h5file.create_table("/", "fourier", FourierDescriptor)
            fourier.cols.vvv_id.create_index()
            h5file.flush()

        server = mpt.TablesServer(h5file)
        print("[WARNING] Writer server will be started in 2 seconds...\n")
        time.sleep(2)
        server.start()

    procs = []
    with mpt.connect(server) as rh5:
        for procno, vvv_ids in chunks:
            proc = ExtractFourier(
                vvv_ids, args.sources, args.periods, rh5, procno)
            proc.start()
            procs.append(proc)
    for proc in procs:
        proc.join()

    print("[WARNING] Writer server will be terminated in 2 seconds...\n")
    #~ time.sleep(2)
    server.terminate()


if __name__ == "__main__":
    main()
