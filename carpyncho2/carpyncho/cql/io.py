#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

import csv
import abc

import six

from corral import util

from . import expressions


# =============================================================================
# AUTO CONSTANTS
# =============================================================================

@six.add_metaclass(abc.ABCMeta)
class Writer(object):

    def __init__(self, query, columns):
        self._query = query
        self._columns = columns

    def dump(self, fp):
        self.setup(fp)
        self.write_row(self._columns, 0)
        for idx, row in enumerate(self._query):
            self.write_row(row, idx+1)
        self.teardown(fp)

    def stream(self, fp):
        self.setup(fp)
        yield self.write_row(self._columns, 0)
        for idx, row in enumerate(self._query):
            yield self.write_row(row, idx+1)
        self.teardown(fp)


    @classmethod
    def fmt(cls):
        return cls.__name__.lower()

    @property
    def query(self):
        return self._query

    @abc.abstractmethod
    def setup(self, fp):
        raise NotImplementedError()

    @abc.abstractmethod
    def write_row(self, row, idx):
        raise NotImplementedError()

    @abc.abstractmethod
    def teardown(self, fp):
        raise NotImplementedError()


class CSV(Writer):

    def setup(self, fp):
        self.writer = csv.writer(fp)

    def write_row(self, row, idx):
        return self.writer.writerow(row)

    def teardown(self, fp):
        pass


# =============================================================================
# FUNCTIONS
# =============================================================================

_WRITERS = {
    cls.fmt(): cls for cls in  util.collect_subclasses(Writer)}

def create_writer(fmt, query, columns):
    if fmt not in expressions.DOWNLOAD_FORMATS:
        raise ValueError("Invalid Format '{}'".format(fmt))
    return _WRITERS[fmt](query, columns)


