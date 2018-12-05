
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

from gatspy.periodic import LombScargleFast, LombScargle

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

class PeriodDescriptor(tb.IsDescription):
    vvv_id = tb.Int64Col(pos=0)
    best_period = tb.FloatCol(pos=1)
    model = tb.StringCol(20, pos=2)

    periods_count = tb.FloatCol(pos=3)
    periods_mean = tb.FloatCol(pos=4)
    periods_std = tb.FloatCol(pos=5)
    periods_min = tb.FloatCol(pos=6)
    periods_25 = tb.FloatCol(pos=7)
    periods_50 = tb.FloatCol(pos=8)
    periods_75 = tb.FloatCol(pos=9)
    periods_max = tb.FloatCol(pos=10)

    power_count = tb.FloatCol(pos=11)
    power_mean = tb.FloatCol(pos=12)
    power_std = tb.FloatCol(pos=13)
    power_min = tb.FloatCol(pos=14)
    power_25 = tb.FloatCol(pos=15)
    power_50 = tb.FloatCol(pos=16)
    power_75 = tb.FloatCol(pos=17)
    power_max = tb.FloatCol(pos=18)


# =============================================================================
# PROCESS
# =============================================================================

class ExtractPeriods(mp.Process):

    def __init__(self, vvv_ids, sources_path, rh5, procno):
        super(ExtractPeriods, self).__init__()
        self.vvv_ids = vvv_ids
        self.sources_path = sources_path
        self.rh5 = rh5
        self.dump_len = 10
        self.procno = procno

    def get_obs(self, vvv_id, obs_table):
        query = "source_id == " + str(int(vvv_id))
        data = []
        for r in obs_table.where(query):
            data.append({k: r[k] for k in obs_table.colnames})
        obs = pd.DataFrame(data)[obs_table.colnames]
        return obs.sort_values("hjd")

    def ls_period(self, time, magnitude, error, prange=(0.2, 1.4), **kwargs):
        if len(time) > 50:
            model = LombScargleFast().fit(time, magnitude, error)
            periods, power = model.periodogram_auto(nyquist_factor=100)
            model.optimizer.period_range = prange
        else:
            model = LombScargle().fit(time, magnitude, error)
            periods, power = model.periodogram_auto(nyquist_factor=100)
            model.optimizer.period_range = prange
        return type(model).__name__, model.best_period, periods, power

    def resume(self, arr):
        q25, q50, q75 = np.percentile(arr, q=(25, 50, 75))
        return [
            len(arr), np.mean(arr), np.std(arr), np.min(arr),
            q25, q50, q75, np.max(arr)]

    def go(self, observations):
        buff, periods = [], self.rh5.get_node("/periods")
        for data_idx, vvv_id in enumerate(self.vvv_ids):
            print("[Storing '{}/p{}'...]".format(data_idx, self.procno))
            obs = self.get_obs(vvv_id, observations)

            model, best_period, ps, power = self.ls_period(
                obs.hjd.values, obs.mag.values, obs.mag_err.values)
            row = (
                [vvv_id, best_period, model] +
                self.resume(ps) + self.resume(power))
            buff.append(row)
            if len(buff) >= self.dump_len:
                periods.append(buff)
                periods.flush()
                buff = []
                break
        if buff:
            periods.append(buff)
            periods.flush()

    def run(self):
        with tb.open_file(self.sources_path) as h5file:
            observations = h5file.get_node("/observations")
            self.go(observations)


# =============================================================================
# RUND
# =============================================================================

def clean(vvv_ids, out_path):
    try:
        periods = pd.read_hdf(out_path, 'periods')
    except (IOError, KeyError):
        pass
    else:
        used = periods.vvv_id.values
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
    sources = clean(sources.id.values, args.out)
    print("[INFO] Found:", len(sources), "sources")

    print("[INFO] Chunk in", args.procs, "process")
    chunks = chunk_it(sources, args.procs)

    with tb.open_file(args.out, mode="a") as h5file:
        if "/periods" not in h5file:
            periods = h5file.create_table("/", "periods", PeriodDescriptor)
            periods.cols.vvv_id.create_index()
            h5file.flush()

        server = mpt.TablesServer(h5file)
        print("[WARNING] Writer server will be started in 2 seconds...\n")
        time.sleep(2)
        server.start()

    procs = []
    with mpt.connect(server) as rh5:
        for procno, vvv_ids in chunks:
            proc = ExtractPeriods(vvv_ids, args.sources, rh5, procno)
            proc.start()
            procs.append(proc)

    for proc in procs:
        proc.join()

    print("[WARNING] Writer server will be terminated in 2 seconds...\n")
    time.sleep(2)
    server.terminate()


if __name__ == "__main__":
    main()
