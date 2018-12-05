#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import tables as tb
import mptables as mpt


PATH = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(PATH, "data", "test.h5")


def p(*args):
    print(" CLIENT   - -", *args)


class Particle(tb.IsDescription):
     name = tb.StringCol(16)   # 16-character String
     idnumber = tb.Int64Col()      # Signed 64-bit integer
     ADCcount = tb.UInt16Col()     # Unsigned short integer
     TDCcount = tb.UInt8Col()      # unsigned byte
     grid_i = tb.Int32Col()      # 32-bit integer
     grid_j = tb.Int32Col()      # 32-bit integer
     pressure = tb.Float32Col()    # float  (single-precision)
     energy = tb.Float64Col()    # double (double-precision)


h5file = tb.open_file(DATA, mode="a")
server = mpt.TablesServer(h5file)
server.start()
time.sleep(2)

# this is convenient to use local
if "/readout" not in h5file:
    table = h5file.create_table("/", 'readout', Particle, "Readout example")
    h5file.flush()


with mpt.connect(server) as rh5:
    p("[PONG]", str(rh5.ping()))
    table = rh5.get_node("/readout")

    rows = []
    for i in range(10):
        particle = {}
        particle['name']  = 'Particle: %6d' % (i)
        particle['TDCcount'] = i % 256
        particle['ADCcount'] = (i * 256) % (1 << 16)
        particle['grid_i'] = i
        particle['grid_j'] = 10 - i
        particle['pressure'] = float(i*i)
        particle['energy'] = float(particle['pressure'] ** 4)
        particle['idnumber'] = i * (2 ** 34)
        rows.append(particle)
        #~ particle.append()
    table.append(rows)





