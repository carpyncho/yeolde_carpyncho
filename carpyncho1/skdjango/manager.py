#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
from django.db import transaction

from model_utils.managers import PassThroughManager

from django_pandas.io import read_frame
from django_pandas.managers import DataFrameQuerySet


# =============================================================================
# FUNCTIONS
# =============================================================================

def commit_after(gen, fnc, ni=100):
    transaction.set_autocommit(False)
    try:
        cnt = 0
        for item in gen:
            cnt += 1
            fnc(item)
            if cnt >= ni:
                transaction.commit()
                cnt = 0
        if cnt != 0:
            transaction.commit()
    except:
        transaction.rollback()
        raise
    finally:
        transaction.set_autocommit(True)


def to_ndarray(qs, fieldnames=(), verbose=True, coerce_float=False):
    df = read_frame(qs, fieldnames=fieldnames, verbose=verbose,
                    index_col=None, coerce_float=coerce_float)
    return df.values


# =============================================================================
# MANAGERS
# =============================================================================

class SciQuerySet(DataFrameQuerySet):

    def to_ndarray(self, fieldnames=(), verbose=True, coerce_float=False):
        return to_ndarray(self, fieldnames, verbose, coerce_float)


class SciManager(PassThroughManager):

    def get_queryset(self):
        return SciQuerySet(self.model)

    get_query_set = get_queryset

