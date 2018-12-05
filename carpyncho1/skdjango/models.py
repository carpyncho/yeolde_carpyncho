#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from django.db import models

import numpy as np
from scipy import stats

from . import extra_stats, manager


# =============================================================================
# STATS MODEL
# =============================================================================

class StatsModelBase(models.base.ModelBase):

    @staticmethod
    def __new__(meta, name, bases, dct):
        if name == "StatsModel":
            return super(StatsModelBase, meta).__new__(meta, name, bases, dct)

        # clean django meta
        dj_meta = dct["Meta"]
        dj_meta_vars = vars(dj_meta)
        stats_from_cls = vars(dj_meta).pop("stats_from")
        stats_query = vars(dj_meta).pop("stats_query")

        dct.update({"stats_from": models.OneToOneField(stats_from_cls)})

        cls = super(StatsModelBase, meta).__new__(meta, name, bases, dct)
        cls._meta.stats_from = stats_from_cls
        cls._meta.stats_query = stats_query

        # change the related name
        related_name = cls.stats_from.field.related.name

        def related_name_fnc(self):
            query = cls.objects.filter(stats_from=self)
            if query.exists():
                return query.get()
            stinst = cls(stats_from=self)
            stinst.calculate()
            stinst.save()
            return stinst

        setattr(stats_from_cls, related_name, property(related_name_fnc))
        return cls


class StatsModel(models.Model):

    __metaclass__ = StatsModelBase

    class Meta:
        abstract = True

    stats_from = None

    recalc = models.BooleanField(default=True)

    obs_number = models.IntegerField(verbose_name="Number of Observations")
    avg = models.FloatField(verbose_name="Average", null=True)
    q25 = models.FloatField(verbose_name="25% Quartile", null=True)
    median = models.FloatField(verbose_name="Median", null=True)
    q75 = models.FloatField(verbose_name="75% Quartile", null=True)
    mode = models.FloatField(verbose_name="Mode", null=True)
    min = models.FloatField(verbose_name="Min Value", null=True)
    max = models.FloatField(verbose_name="Max Value", null=True)
    sum = models.FloatField(verbose_name="Sum", null=True)
    Q = models.FloatField(verbose_name="Quartile Average", null=True)
    TRI = models.FloatField(verbose_name="Trimedian", null=True)
    MID = models.FloatField(verbose_name="Intra Quartile Average", null=True)

    var = models.FloatField(verbose_name="Variance", null=True)
    std = models.FloatField(verbose_name="Std Deviation", null=True)
    range = models.FloatField(verbose_name="Range", null=True)
    MD = models.FloatField(verbose_name="Average Deviation", null=True)
    MeD = models.FloatField(verbose_name="Median Deviation", null=True)

    variation = models.FloatField(
        verbose_name="Variation Coeficient", null=True)
    varQ = models.FloatField(verbose_name="Intra Quatile deviation", null=True)

    Sp_pearson = models.FloatField(verbose_name="Pearson Asymetry", null=True)
    H1_yule = models.FloatField(verbose_name="Yule Asymetry", null=True)
    H3_kelly = models.FloatField(verbose_name="Kelly Asymetry", null=True)

    K1_kurtosis = models.FloatField(verbose_name="Robust Kurtosis", null=True)
    kurtosis = models.FloatField(verbose_name="Kurtosis", null=True)
    kurtosis_test_z_score = models.FloatField(
        verbose_name="Kurtosis Test Z-Score", null=True
    )
    kurtosis_test_p_value = models.FloatField(
        verbose_name="Kurtosis Test P-Value", null=True
    )

    objects = manager.SciManager()

    def dataset(self):
        return self._meta.stats_query(self.stats_from)

    def calculate(self):

        if not self.recalc:
            raise ValueError("Please set recalc to True")

        data = np.array(self.dataset() or [])
        self.obs_number = len(data)
        self.recalc = False

        if self.obs_number == 0:
            return

        self.avg = np.average(data)
        self.q25, self.median, self.q75 = np.percentile(data, (25, 50, 75))
        modedata = stats.mode(data)
        if modedata[1][0] > 1:
            self.mode = modedata[0][0]
        self.min = np.min(data)
        self.max = np.max(data)
        self.sum = np.sum(data)
        self.Q = extra_stats.Q(data)
        self.TRI = extra_stats.TRI(data)
        self.MID = extra_stats.MID(data)

        self.var = np.var(data)
        self.std = np.std(data)
        self.range = extra_stats.range(data)
        self.MD = extra_stats.MD(data)
        self.MeD = extra_stats.MeD(data)

        self.variation = stats.variation(data)
        self.varQ = extra_stats.varQ(data)

        if self.obs_number > 1:
            self.Sp_pearson = extra_stats.Sp_pearson(data)
            self.H1_yule = extra_stats.H1_yule(data)
            self.H3_kelly = extra_stats.H3_kelly(data)
        else:
            self.Sp_pearson = None
            self.H1_yule = None
            self.H3_kelly = None

        self.kurtosis = stats.kurtosis(data)

        if self.obs_number >= 20:
            self.kurtosis_test_z_score, self.kurtosis_test_p_value = (
                stats.kurtosistest(data)
            )
        else:
            self.kurtosis_test_z_score, self.kurtosis_test_p_value = None, None


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
