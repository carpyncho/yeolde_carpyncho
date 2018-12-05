#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""This file is for distribute yatel with distutils

"""

#==============================================================================
# IMPORTS
#==============================================================================

import os

#==============================================================================
# CONSTANTS
#==============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS_PATH = os.path.join(PATH, "requirements.txt")

with open(REQUIREMENTS_PATH) as fp:
    REQUIREMENTS = [line.strip() for line in fp.readlines() if line.strip()]


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    import sys

    from ez_setup import use_setuptools
    use_setuptools()

    from setuptools import setup, find_packages

    setup(
        name="carpyncho",
        version="dev",
        description="Integration tool for load and analize data from vvv",
        author="Cabral, Juan",
        author_email="jbc.develop@gmail.com",
        url="http://carpyncho.vvv-tools.com.ar/",
        license="WISKEY-WARE",
        keywords="astronomy vvv",
        #~ classifiers=yatel.CLASSIFIERS,
        packages=[pkg for pkg in find_packages() if pkg.startswith("carpyncho")],
        include_package_data=True,
        py_modules=["ez_setup", "manage"],
        entry_points={'console_scripts': ['pyncho = manage:run_manager']},
        install_requires=REQUIREMENTS,
    )
