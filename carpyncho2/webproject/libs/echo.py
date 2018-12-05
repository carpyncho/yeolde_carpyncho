#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        if value:
            return value
