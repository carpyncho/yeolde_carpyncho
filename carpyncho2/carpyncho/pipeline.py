#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-07T20:41:54.110455 by corral 0.0.1


# =============================================================================
# DOCS
# =============================================================================

"""carpyncho dynamic configurations

"""

# =============================================================================
# IMPORTS
# =============================================================================

import logging
import os

from corral.setup import PipelineSetup
from corral.conf import settings


# =============================================================================
# CONFIGURATION
# =============================================================================

class Pipeline(PipelineSetup):
    """Pipeline for make a machine learning facility over VVV Data

    - Homepage: http://carpyncho.jbcabral.org
    - Contact: jbc.develop@gmail.com
    - IATE-OAC-UNC, FCEIA-UNR, CONICET

    """


    name = "Carpyncho Pipeline"

    def setup(self):
        self.default_setup()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
        if not os.path.exists(settings.STORED_TILES_DIR):
            os.makedirs(settings.STORED_TILES_DIR)

        if not os.path.exists(settings.STORED_PAWPRINT_DIR):
            os.makedirs(settings.STORED_PAWPRINT_DIR)
