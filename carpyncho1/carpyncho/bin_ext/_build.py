#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

PATH = os.path.abspath(os.path.dirname(__file__))

commands = "\n".join([
    l.strip() for l in
    """
        set -e;
        cd {};
        gfortran fitsio_cat_list.f -o fitsio_cat_list -L/sw/lib -lcfitsio -lm;
        gfortran tff.f -o tff;
        cd -;

    """.format(PATH).splitlines()
]).strip()


def build():
    os.system(commands)
