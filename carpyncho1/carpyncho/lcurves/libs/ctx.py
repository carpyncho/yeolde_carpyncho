#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import contextlib
import sys

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


@contextlib.contextmanager
def silence_stdout(silence=True):
    old = sys.stdout
    if silence:
        sys.stdout = StringIO()
    try:
        yield
    finally:
        if silence:
            sys.stdout = old
