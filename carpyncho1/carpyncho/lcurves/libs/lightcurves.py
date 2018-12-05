#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import six

import numpy as np

from scipy.stats import norm

import pandas as pd

from PyAstronomy.pyTiming import pyPDM, pyPeriod

from gatspy.periodic import LombScargleFast

from . import ctx


# =============================================================================
# CONSTANTS
# =============================================================================

SILENCE = True


def pdm_period(time, magnitude, error=None, **kwargs):

    # scanner creation
    sparams = {"minVal": 0.01, "maxVal": 1, "dVal": 0.001}
    sparams.update(kwargs)
    sparams["mode"] = "period"
    scanner = pyPDM.Scanner(**sparams)

    pdm = pyPDM.PyPDM(time, magnitude)
    periods, frequencies = pdm.pdmEquiBin(20, scanner)
    period = periods[np.argmin(frequencies)]

    return period


def ls_period(time, magnitude, error, prange=(0.2, 1.4), **kwargs):
    with ctx.silence_stdout(SILENCE):
        model = LombScargleFast().fit(time, magnitude, error)
        periods, power = model.periodogram_auto(nyquist_factor=100)

        model.optimizer.period_range = prange
        return model.best_period, (periods, power)


def phase(time, magnitude, period):
    phase = ((time - time[0])/period) - np.floor((time - time[0])/period)
    return phase


def duplicate(x, y):
    x_d = np.append(x, x + 1)
    y_d = np.tile(y, 2)
    return x_d, y_d


def montecarlo_pc(time, magnitude, error, n=10, p_calculator="ls", **kwargs):
    if p_calculator == "ls":
        p_calculator = lambda *args, **kwargs: ls_period(*args, **kwargs)[0]
    elif p_calculator == "pdm":
        p_calculator = pdm_period
    else:
        raise ValueError("'p_calulator' must be 'ls' (LombScargle) or 'pdm'")
    size = len(time)
    periods = np.empty(n)
    for idx in six.moves.range(n):
        random = np.random.rand(size)
        vmagnitude = norm.ppf(random, magnitude, scale=error)
        periods[idx] = p_calculator(time, vmagnitude, error, **kwargs)
    return pd.DataFrame(periods)
