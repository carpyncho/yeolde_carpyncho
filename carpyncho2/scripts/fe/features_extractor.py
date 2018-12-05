
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

import mock

import numpy as np

import pandas as pd

import pytff

import tables as tb

from libs import mptables as mpt

import FATS


# =============================================================================
# SUPRESS WARNINGS
# =============================================================================

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


# =============================================================================
# SA
# =============================================================================

class FeaturesDescriptor(tb.IsDescription):
    vvv_id = tb.Int64Col(pos=0)
    cls = tb.Int64Col(pos=1)

    Amplitude = tb.FloatCol(pos=2)
    Rcs = tb.FloatCol(pos=3)
    StetsonK = tb.FloatCol(pos=4)
    Meanvariance = tb.FloatCol(pos=5)
    Autocor_length = tb.FloatCol(pos=6)
    #~ SlottedA_length = tb.FloatCol(pos=7)
    StetsonK_AC = tb.FloatCol(pos=8)
    Con = tb.FloatCol(pos=9)
    Beyond1Std = tb.FloatCol(pos=10)
    SmallKurtosis = tb.FloatCol(pos=11)
    Std = tb.FloatCol(pos=12)
    Skew = tb.FloatCol(pos=13)
    MaxSlope = tb.FloatCol(pos=14)
    MedianAbsDev = tb.FloatCol(pos=15)
    MedianBRP = tb.FloatCol(pos=16)
    PairSlopeTrend = tb.FloatCol(pos=17)
    FluxPercentileRatioMid20 = tb.FloatCol(pos=18)
    FluxPercentileRatioMid35 = tb.FloatCol(pos=19)
    FluxPercentileRatioMid50 = tb.FloatCol(pos=20)
    FluxPercentileRatioMid65 = tb.FloatCol(pos=21)
    FluxPercentileRatioMid80 = tb.FloatCol(pos=22)
    PercentDifferenceFluxPercentile = tb.FloatCol(pos=23)
    PercentAmplitude = tb.FloatCol(pos=24)
    LinearTrend = tb.FloatCol(pos=25)
    Eta_e = tb.FloatCol(pos=26)
    Mean = tb.FloatCol(pos=27)
    Q31 = tb.FloatCol(pos=28)
    AndersonDarling = tb.FloatCol(pos=29)
    PeriodLS = tb.FloatCol(pos=30)
    Period_fit = tb.FloatCol(pos=31)
    Psi_CS = tb.FloatCol(pos=32)
    Psi_eta = tb.FloatCol(pos=33)
    CAR_sigma = tb.FloatCol(pos=34)
    CAR_tau = tb.FloatCol(pos=35)
    CAR_mean = tb.FloatCol(pos=36)
    Freq1_harmonics_amplitude_0 = tb.FloatCol(pos=37)
    Freq1_harmonics_amplitude_1 = tb.FloatCol(pos=38)
    Freq1_harmonics_amplitude_2 = tb.FloatCol(pos=39)
    Freq1_harmonics_amplitude_3 = tb.FloatCol(pos=40)
    Freq2_harmonics_amplitude_0 = tb.FloatCol(pos=41)
    Freq2_harmonics_amplitude_1 = tb.FloatCol(pos=42)
    Freq2_harmonics_amplitude_2 = tb.FloatCol(pos=43)
    Freq2_harmonics_amplitude_3 = tb.FloatCol(pos=44)
    Freq3_harmonics_amplitude_0 = tb.FloatCol(pos=45)
    Freq3_harmonics_amplitude_1 = tb.FloatCol(pos=46)
    Freq3_harmonics_amplitude_2 = tb.FloatCol(pos=47)
    Freq3_harmonics_amplitude_3 = tb.FloatCol(pos=48)
    Freq1_harmonics_rel_phase_0 = tb.FloatCol(pos=49)
    Freq1_harmonics_rel_phase_1 = tb.FloatCol(pos=50)
    Freq1_harmonics_rel_phase_2 = tb.FloatCol(pos=51)
    Freq1_harmonics_rel_phase_3 = tb.FloatCol(pos=52)
    Freq2_harmonics_rel_phase_0 = tb.FloatCol(pos=53)
    Freq2_harmonics_rel_phase_1 = tb.FloatCol(pos=54)
    Freq2_harmonics_rel_phase_2 = tb.FloatCol(pos=55)
    Freq2_harmonics_rel_phase_3 = tb.FloatCol(pos=56)
    Freq3_harmonics_rel_phase_0 = tb.FloatCol(pos=57)
    Freq3_harmonics_rel_phase_1 = tb.FloatCol(pos=58)
    Freq3_harmonics_rel_phase_2 = tb.FloatCol(pos=59)
    Freq3_harmonics_rel_phase_3 = tb.FloatCol(pos=60)

    gatspy_period = tb.FloatCol(pos=61)
    count = tb.Int64Col(pos=62)

UNK_STAR_TYPE = -1

STAR_TYPES = {
    "RRab": 1,
    "RRc": 2,
    "RRd": 3,
    "INVARIABLE": 0,
}


# =============================================================================
# PROCESS
# =============================================================================

class ExtractFeatures(mp.Process):

    def __init__(self, vvv_ids, sources_path, periods_path, fourier_path, cls_path, rh5, procno):
        super(ExtractFeatures, self).__init__()
        self.vvv_ids = vvv_ids
        self.sources_path = sources_path
        self.periods_path = periods_path
        self.fourier_path = fourier_path
        self.cls_path = cls_path
        self.rh5 = rh5
        self.procno = procno
        self.dump_len = 100
        self.columns_order = self.get_columns_order()

    def get_columns_order(self):
        columns = [
            (cname, column._get_init_args()["pos"])
            for cname, column in FeaturesDescriptor.columns.items()]
        return tuple(c[0] for c in sorted(columns, key=lambda c: c[1]))

    def get_obs(self, vvv_id, obs_table):
        query = "source_id == {}".format(int(vvv_id))
        rows = obs_table.read_where(query)[:]
        mags, hjds, mag_errs = (rows["mag"], rows["hjd"], rows["mag_err"])
        order = mags.argsort()
        mags, hjds, mag_errs = mags[order], hjds[order], mag_errs[order]
        return np.vstack((mags, hjds, mag_errs)), len(mags)

    def get_cls(self, vvv_id, data, cls_table):
        query = "vvv_id == {}".format(int(vvv_id))
        row = cls_table.read_where(query)
        if len(row):
            star_type = row["star_type"][0]
            return {"cls": STAR_TYPES[star_type]}
        return {"cls": UNK_STAR_TYPE}

    def get_periods_info(self, vvv_id, p_table):
        query = "vvv_id == {}".format(int(vvv_id))
        row = p_table.read_where(query)[0]
        Qmean = (row["power_25"] + row["power_75"]) / 2.
        data = {"gatspy_period": row["best_period"]}
        return data

    def go(self, observations_table, periods_table, fourier_table, cls_table):
        buff, features = [], self.rh5.get_node("/features")
        for data_idx, vvv_id in enumerate(self.vvv_ids):
            print("[Storing '{}/p{}'...]".format(data_idx, self.procno))
            data = {"vvv_id": vvv_id}
            obs, count = self.get_obs(vvv_id, observations_table)
            data.update(self.get_periods_info(vvv_id, periods_table))
            data["count"] = count

            with mock.patch("sys.stdout"), warnings.catch_warnings():
                fats = FATS.FeatureSpace(
                    Data=["magnitude", 'time', 'error'],
                    excludeList=["SlottedA_length"])
                result = fats.calculateFeature(obs)
            data.update(result.result(method="dict"))
            data.update(self.get_cls(vvv_id, data, cls_table))

            #~ with open("foo.txt", "w") as fp:
                #~ for k in data.keys():
                    #~ fp.write(k + "\n")

            row = [data[cn] for cn in self.columns_order]
            buff.append(row)
            if len(buff) >= self.dump_len:
                features.append(buff)
                features.flush()
                buff = []
                break
        if buff:
            features.append(buff)
            features.flush()

    def run(self):
        with tb.open_file(self.sources_path) as obs_file, \
             tb.open_file(self.periods_path) as per_file, \
             tb.open_file(self.fourier_path) as fou_file, \
             tb.open_file(self.cls_path) as cls_file:
                observations = obs_file.get_node("/observations")
                periods = per_file.get_node("/periods")
                fourier = fou_file.get_node("/fourier")
                clss = cls_file.get_node("/vvv_x_ogle").table
                self.go(observations, periods, fourier, clss)


# =============================================================================
# RUND
# =============================================================================

def clean(vvv_ids, out_path):
    try:
        features = pd.read_hdf(out_path, 'features')
    except (IOError, KeyError):
        pass
    else:
        used = features.vvv_id.values
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
    parser = argparse.ArgumentParser(description='Extract features components')
    parser.add_argument(
        '--sources', dest="sources", required=True,
        metavar='PATH', type=os.path.abspath,
        help='an h5 file dump from carpyncho')
    parser.add_argument(
        '--periods', dest="periods", metavar='PATH', required=True,
        type=os.path.abspath, help='an h5 file of periods')
    parser.add_argument(
        '--fourier', dest="fourier", metavar='PATH', required=True,
        type=os.path.abspath, help='an h5 file of fourier components')
    parser.add_argument(
        '--cls', dest="cls", metavar='PATH', required=True,
        type=os.path.abspath, help='an h5 file of classes')
    parser.add_argument(
        '--out', dest="out", metavar="PATH",
        type=os.path.abspath, required=True, help='h5 file to write into')
    parser.add_argument(
        '-p', "--procs", dest="procs", default=1,
        help="Number of process to span")
    parser.add_argument(
        "--sync", dest="sync", action="store_true",
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
        if "/features" not in h5file:
            features = h5file.create_table("/", "features", FeaturesDescriptor)
            features.cols.vvv_id.create_index()
            features.cols.cls.create_index()
            h5file.flush()

        server = mpt.TablesServer(h5file)
        print("[WARNING] Writer server will be started in 2 seconds...\n")
        time.sleep(2)
        server.start()

    procs = []
    with mpt.connect(server) as rh5:
        for procno, vvv_ids in chunks:
            proc = ExtractFeatures(
                vvv_ids, args.sources, args.periods, args.fourier,
                args.cls, rh5, procno)
            if args.sync:
                proc.run()
            else:
                proc.start()
                procs.append(proc)
    for proc in procs:
        proc.join()

    print("[WARNING] Writer server will be terminated in 2 seconds...\n")
    time.sleep(2)
    server.terminate()


if __name__ == "__main__":
    main()
