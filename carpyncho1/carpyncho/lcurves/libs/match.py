#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import copy
import tempfile
import shutil

import numpy as np

from astropysics import coords

from carpyncho import bin_ext


#==============================================================================
# CONSTANTS
#==============================================================================

# 1 arc second
MAX_MATCH = 3 * 9.2592592592592588e-5


PAWPRINTS_DEFAULT_PARAMS = {
    "dtype": {
        'names': [
            'ra_h', 'ra_m', 'ra_s', 'dec_d', 'dec_m', 'dec_s',
            'x', 'y', 'mag', 'mag_err',
            'chip_nro', 'stel_cls', 'elip', 'pos_ang',
        ],
        'formats': [
            'i4', 'i4', 'f4', 'i4', 'i4', 'f4',
            'f4', 'f4', 'f4', 'f4',
            'i4', 'i4', 'f4', 'f4',
        ]
    }
}

MASTER_SOURCE_DEFAULT_PARAMS = {
    "dtype": {
        'names': (
            'ra_h', 'dec_h', 'ra_j', 'dec_j', 'ra_k', 'dec_k'
        ),
        'formats': (
            'f4', 'f4', 'f4', 'f4', 'f4', 'f4'
        )
    },
    "usecols": [0, 1, 2, 3, 4, 5],
}


#==============================================================================
# CLASSES
#==============================================================================

class LCurvesCommandError(Exception):

    def __init__(self, cmd, err, out, errcode):
        self.cmd = u" ".join(cmd)
        self.err = err
        self.out = out
        self.errcode = errcode
        msg = "\n".join([
            u"Error running '{}'".format(self.cmd),
            u"Err: {}".format(self.err),
            u"Out: {}".format(self.out),
            u"Exit Status: {}".format(self.errcode)
        ])
        super(LCurvesCommandError, self).__init__(msg)


#==============================================================================
# FUNCTIONS
#==============================================================================

def ra_to_degree(catalogs):
    """Conviert el ra en grados

    """
    return  15 * (
        catalogs['ra_h'] +
        catalogs['ra_m'] / 60.0 +
        catalogs['ra_s'] / 3600.0
    )


def dec_to_degree(catalogs):
    """Extrae la declinacion en forme grados

    """

    return np.sign(catalogs['dec_d']) * (
       np.abs(catalogs['dec_d']) +
       catalogs['dec_m'] / 60.0 +
       catalogs['dec_s'] / 3600.0
    )


def execute(command):
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = [x.decode("utf-8") for x in proc.communicate()]
    if proc.returncode:
        raise LCurvesCommandError(command, err, out, proc.returncode)
    return out


def read_mastersrc(fp, epochs=3,
                   wfilter=lambda arr: arr["ra_k"] > -9999.0, **kwargs):
    """Read the master source and return the array with the data

    master = read_mastersrc(
        open("cat_b264_jhk_1.dat"),

    )

    """
    rkwargs = copy.deepcopy(MASTER_SOURCE_DEFAULT_PARAMS)
    rkwargs.update(kwargs)
    arr = np.genfromtxt(fp, skiprows=epochs, **rkwargs)
    if wfilter:
        flt = wfilter(arr)
        arr = arr[flt]
    return arr


def read_pawprint(fp, **kwargs):
    """

    read_pawprint(
        open("file.fits")

    # patch arguments
    """

    rkwargs = copy.deepcopy(PAWPRINTS_DEFAULT_PARAMS)
    rkwargs.update(kwargs)

    fd, fname = tempfile.mkstemp()

    cmd = [bin_ext.get("fitsio_cat_list"), fname]
    catalogue_asc_path = os.path.join(os.getcwd(), "catalogue.asc")
    try:
        shutil.copyfile(fp.name, fname)

        execute(cmd)
        odata = np.genfromtxt(catalogue_asc_path, **rkwargs)
        ra_deg = ra_to_degree(odata)
        dec_deg = dec_to_degree(odata)

        conf = copy.deepcopy(rkwargs)
        conf["dtype"]["names"].insert(0, "dec_deg")
        conf["dtype"]["names"].insert(0, "ra_deg")
        conf["dtype"]["formats"].insert(0, "f4")
        conf["dtype"]["formats"].insert(0, "f4")

        data = np.empty(len(odata), **conf)
        for name in data.dtype.names:
            if name == "ra_deg":
                data[name] = ra_deg
            elif name == "dec_deg":
                data[name] = dec_deg
            else:
                data[name] = odata[name]
    finally:
        os.close(fd)
        if os.path.isfile(catalogue_asc_path):
#            os.remove(catalogue_asc_path)
            pass
        if os.path.isfile(fname):
            os.remove(fname)
    return data


def create_match(data_ms, data_pwp, maxmatch=None, mode="nearest"):
    """Genera una tabla con datos cruzados entre el master_src y el pwprint

    """
    maxmatch = maxmatch or MAX_MATCH

    nearestind_pwp, distance_pwp, match_pwp = coords.match_coords(
        data_ms["ra_k"], data_ms["dec_k"],
        data_pwp["ra_deg"], data_pwp["dec_deg"],
        eps=maxmatch, mode=mode
    )
    nearestind_ms, distance_ms, match_ms = coords.match_coords(
        data_pwp["ra_deg"], data_pwp["dec_deg"],
        data_ms["ra_k"], data_ms["dec_k"],
        eps=maxmatch, mode=mode
    )
    match = []
    for idx_pwp, idx_ms in enumerate(nearestind_ms):
        if match_ms[idx_pwp] and \
           nearestind_pwp[idx_ms] == idx_pwp \
           and match_pwp[idx_ms]:
                match.append((idx_ms, idx_pwp))
    return tuple(match)


#==============================================================================
# MAIN
#==============================================================================

def _main(args):
    pass


if __name__ == "__main__":
    print(__doc__)
