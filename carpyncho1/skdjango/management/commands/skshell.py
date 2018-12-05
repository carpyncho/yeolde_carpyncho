#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Move data

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

from django_extensions.management import shells
from django_extensions.management.shells import import_objects as _oio

from ... import extra_stats as estats


#==============================================================================
# PATCH IMPORT OBJECTS
#==============================================================================

def sk_import_objects(*args, **kwargs):
    data = _oio(*args, **kwargs)
    data.update(np=np, plt=plt, stats=stats, estats=estats, pd=pd)
    return data

shells.import_objects = sk_import_objects


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("carpyncho")


#==============================================================================
# COMMAND
#==============================================================================

from django_extensions.management.commands import shell_plus

class Command(shell_plus.Command):
    pass


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
