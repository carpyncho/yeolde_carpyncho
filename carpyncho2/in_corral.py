#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-07T20:41:54.110455 by corral 0.0.1


if __name__ == "__main__":
    import os

    os.environ.setdefault("CORRAL_SETTINGS_MODULE", "carpyncho.settings")

    from corral import cli
    cli.run_from_command_line()
