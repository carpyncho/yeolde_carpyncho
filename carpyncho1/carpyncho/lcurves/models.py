#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from picklefield.fields import PickledObjectField

import numpy as np

from PyAstronomy import pyasl

from save_the_change.mixins import SaveTheChange

from carpyncho.utils import storages

from skdjango.models import StatsModel
from skdjango.manager import SciManager

from carpyncho.lcurves.libs import match, lightcurves
from .manager import MasterSourceManager


# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger("lcurves")

# =============================================================================
# CLASIFICATIONS
# =============================================================================

class Clasification(SaveTheChange, models.Model):

    name = models.CharField(
        max_length=255, verbose_name=_("Name"), unique=True
    )

    objects = SciManager()

    def __unicode__(self):
        return self.name


#==============================================================================
# TILE
#==============================================================================

def masters_upload(master, filename):
    return u"/".join(["lcurves", master.name, filename])


class Tile(SaveTheChange, models.Model):
    class Meta:
        verbose_name = _("Tile")
        verbose_name_plural = _("Tile")

    file = models.FileField(
        upload_to=masters_upload, verbose_name=_("File"),
        storage=storages.OverwriteStorage()
    )
    name = models.CharField(
        max_length=255, verbose_name=_("Name"), unique=True
    )

    objects = SciManager()

    def __unicode__(self):
        return self.name


#==============================================================================
# MASTER SOURCE
#==============================================================================

class MasterSource(SaveTheChange, models.Model):
    class Meta:
        verbose_name = _("Master Source")
        verbose_name_plural = _("Masters Sources")
        unique_together = ["tile", "order"]

    tile = models.ForeignKey(
        Tile, related_name="sources", verbose_name=_("Tile")
    )

    order = models.IntegerField(verbose_name=_("Order"))

    ra_h = models.FloatField(verbose_name=_("RA H"))
    dec_h = models.FloatField(verbose_name=_("Dec H"))

    ra_j = models.FloatField(verbose_name=_("RA J"))
    dec_j = models.FloatField(verbose_name=_("Dec J"))

    ra_k = models.FloatField(verbose_name=_("RA K"))
    dec_k = models.FloatField(verbose_name=_("Dec K"))

    x = models.FloatField(verbose_name=_("Y"))
    y = models.FloatField(verbose_name=_("X"))
    z = models.FloatField(verbose_name=_("Z"))

    clasifications = models.ManyToManyField(
        Clasification, verbose_name="Clasifications", related_name="sources",
        help_text=_("Identify diferents clasifications of the same source for internal propuses"),
        through="ClasificationXMasterSource"
    )

    type = models.CharField(
        max_length=255, verbose_name=_("Type"), default=None, null=True,
        choices=[(e, e) for e in sorted(settings.SOURCES_TYPES)],
        help_text=_("This identify the source type")
    )

    objects = MasterSourceManager()

    def __unicode__(self):
        return u"{}[{}]".format(self.tile, self.order)


class ClasificationXMasterSource(SaveTheChange, models.Model):
    class Meta:
        unique_together = ["master_src", "clasification"]

    master_src = models.ForeignKey(MasterSource)
    clasification = models.ForeignKey(Clasification)
    extra_data = PickledObjectField()

    objects = SciManager()

    def __unicode__(self):
        return u"{}: {}".format(
            unicode(self.clasification), unicode(self.master_src))


class MagStats(StatsModel):
    class Meta:
        stats_from = MasterSource

        def stats_query(master_src):
            return master_src.matches.values_list(
                "pawprint_src__mag", flat=True)


class MagErrStats(StatsModel):
    class Meta:
        stats_from = MasterSource

        def stats_query(master_src):
            return master_src.matches.values_list(
                "pawprint_src__mag_err", flat=True)



# =============================================================================
# LCurve
# =============================================================================

class LightCurve(SaveTheChange, models.Model):

    source = models.OneToOneField(MasterSource, related_name="+")

    recalc = models.BooleanField(default=True)
    obs_number = models.IntegerField(verbose_name="Number of Observations")
    pdm_period = models.FloatField(verbose_name=_("PDM Period"), null=True, default=None)
    ls_period = models.FloatField(verbose_name=_("Lomb-Scargle Period"), null=True, default=None)

    objects = SciManager()

    def __unicode__(self):
        return unicode(self.source)

    def dataset(self):
        if not hasattr(self, "_dataset"):
            self._dataset = self.source.matches.all().order_by(
                "pawprint_src__pawprint__mjd"
            ).values(
                "pawprint_src__pawprint__mjd",
                "pawprint_src__mag", "pawprint_src__mag_err")
        return self._dataset

    def time(self):
        dataset = self.dataset()
        return dataset.to_ndarray(["pawprint_src__pawprint__mjd"]).ravel()

    def magnitude(self):
        dataset = self.dataset()
        return dataset.to_ndarray(["pawprint_src__mag"]).ravel()

    def magnitude_error(self):
        dataset = self.dataset()
        return dataset.to_ndarray(["pawprint_src__mag_err"]).ravel()

    def calculate(self):
        if not self.recalc:
            raise ValueError("Please set recalc to True")

        self.recalc = False
        dataset = self.dataset()
        self.obs_number = dataset.count()
        if self.obs_number > 0:
            time, magnitude, error = (
                self.time(), self.magnitude(), self.magnitude_error())
            self.pdm_period = lightcurves.pdm_period(time, magnitude)
            self.ls_period = lightcurves.ls_period(time, magnitude, error)


def _lightcurve(self):
    query = LightCurve.objects.filter(source=self)
    if query.exists():
        return query.get()
    lc = LightCurve(source=self)
    lc.calculate()
    lc.save()
    return lc

MasterSource.lightcurve = property(_lightcurve)
del _lightcurve


#==============================================================================
# PAWPRINT
#==============================================================================

def pwprints_upload(pwprint, filename):
    subfolder = pwprint.name.split("_", 1)[0]
    return u"/".join(["lcurves", "pawprints", subfolder, filename])

class Pawprint(SaveTheChange, models.Model):
    class Meta:
        verbose_name = _("Pawprint")
        verbose_name_plural = _("Pawprints")

    tile = models.ManyToManyField(
        Tile, related_name="pawprints",
        verbose_name=_("Tile"), through="PawprintXModel"
    )
    file = models.FileField(
        upload_to=pwprints_upload, verbose_name=_("File"),
        storage=storages.OverwriteStorage()
    )
    name = models.CharField(
        max_length=255, verbose_name=_("Name"), unique=True
    )
    mjd = models.FloatField(verbose_name=_("MJD"), null=True, default=None)
    has_sources = models.BooleanField(default=False)

    objects = SciManager()

    def sync_resume(self):
        return self.pawprintxmodel_set.all().values_list("tile__name", "sync")

    def rescan_sources(self):
        if self.has_sources:
            raise Exception("This pawprint already has sources")

        if self.sources.exists():
            self.sources.all().delete()

        logger.info(u"Loading sources...")
        with open(self.file.path, "rb") as fp:
            for order, src in enumerate(match.read_pawprint(fp)):
                srcmodel = PawprintSource(
                    pawprint=self, order=order,
                    ra_deg=src[0], dec_deg=src[1],
                    ra_h=src[2], ra_m=src[3], ra_s=src[4],
                    dec_d=src[5], dec_m=src[6], dec_s=src[7],
                    pwp_x=src[8], pwp_y=src[9], mag=src[10], mag_err=src[11],
                    chip_nro=src[12], stel_cls=src[13],
                    elip=src[14], pos_ang=src[15],
                    hjd=pyasl.helio_jd(self.mjd, src[0], src[1])
                )
                str_order = str(order)[1:]
                if  len(str_order) == str_order.count("0"):
                    logger.info("Pawprint Source number: {}".format(order))
                srcmodel.save()

    def __unicode__(self):
        tilenames = ",".join(self.tile.all().values_list("name", flat=True))
        return u"({}).{}".format(tilenames, self.name)


class PawprintXModel(SaveTheChange, models.Model):
    class Meta:
        unique_together = ["tile", "pawprint"]

    tile = models.ForeignKey(Tile)
    pawprint = models.ForeignKey(Pawprint)
    matched = models.BooleanField(verbose_name=_("Matched"), default=False)

    objects = SciManager()

    def ms_dataset(self):
        if not hasattr(self, "__ms_dataset"):
            self.__ms_dataset = self.tile.sources.values_list(
                "id", "ra_k", "dec_k").order_by("order")
        return self.__ms_dataset

    def data_ms(self):
        dataset = self.ms_dataset().to_ndarray().T
        return np.core.records.fromarrays(
            dataset, dtype=[("pk", 'i4'), ("ra_k", 'f4'), ("dec_k", 'f4')])


    def pwp_dataset(self):
        if not hasattr(self, "__pwp_dataset"):
            self.__pwp_dataset = self.pawprint.sources.values_list(
                    "id", "ra_deg", "dec_deg").order_by("order")
        return self.__pwp_dataset

    def data_pwp(self):
        dataset = self.pwp_dataset().to_ndarray().T
        return np.core.records.fromarrays(
            dataset, dtype=[("pk", 'i4'), ("ra_deg", 'f4'), ("dec_deg", 'f4')])

    def match(self, data_ms=None, data_pwp=None):
        if self.matched:
            raise Exception("This pawprint is already matched with this tile")

        old_matches = Match.objects.filter(
            master_src__tile=self.tile, pawprint_src__pawprint=self.pawprint
        )
        if old_matches.exists():
            old_matches.delete()
        del old_matches

        data_ms = data_ms if data_ms is not None else self.data_ms()
        data_pwp = data_pwp if data_pwp is not None else self.data_pwp()

        matches = match.create_match(data_ms, data_pwp)
        logger.info(u"'{}' matches".format(len(matches)))
        logger.info(u"Writing matches")
        for order_ms, order_pwp in matches:
            master_src = self.tile.sources.get(pk=data_ms[order_ms]["pk"])
            pawprint_src = self.pawprint.sources.get(
                pk=data_pwp[order_pwp]["pk"])
            Match.objects.create(
                master_src=master_src, pawprint_src=pawprint_src
            )


#==============================================================================
# PAWPRINT SOURCE
#==============================================================================

class PawprintSource(SaveTheChange, models.Model):
    class Meta:
        verbose_name = _("Pawprint Source")
        verbose_name_plural = _("Pawprints Sources")
        unique_together = ["pawprint", "order"]

    pawprint = models.ForeignKey(
        Pawprint, related_name="sources", verbose_name=_("Pawprint")
    )
    order = models.IntegerField(verbose_name=_("Order"))
    ra_deg = models.FloatField(verbose_name=_("RA Deg"))
    ra_h = models.IntegerField(verbose_name=_("RA H"))
    ra_m = models.IntegerField(verbose_name=_("RA m"))
    ra_s = models.FloatField(verbose_name=_("RA s"))
    dec_deg = models.FloatField(verbose_name=_("Dec Deg"))
    dec_d = models.IntegerField(verbose_name=_("Dec D"))
    dec_m = models.IntegerField(verbose_name=_("Dec m"))
    dec_s = models.FloatField(verbose_name=_("Dec s"))
    pwp_x = models.FloatField(verbose_name=_("Pawprint X"))
    pwp_y = models.FloatField(verbose_name=_("Pawprint Y"))
    mag = models.FloatField(verbose_name=_("Mag"))
    mag_err = models.FloatField(verbose_name=_("Mag Err"))
    chip_nro = models.IntegerField(verbose_name=_("Chip Nro"))
    stel_cls = models.IntegerField(verbose_name=_("Stellar Class"))
    elip = models.FloatField(verbose_name=_("Elip"))
    pos_ang = models.FloatField(verbose_name=_("Pos. Ang."))
    hjd = models.FloatField(verbose_name=_("HJD"), null=True, default=None)

    objects = SciManager()

    def __unicode__(self):
        return u"{}[{}]".format(self.pawprint, self.order)


#==============================================================================
# MATCH
#==============================================================================

class Match(SaveTheChange, models.Model):

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matchs")
        unique_together = ("master_src", "pawprint_src")

    master_src = models.ForeignKey(
        MasterSource, related_name="matches", verbose_name=_("Pawprint Source")
    )
    pawprint_src =models.ForeignKey(
        PawprintSource, related_name="matches", verbose_name=_("Master Source")
    )

    ra_avg = models.FloatField(verbose_name="Ra Degree Average")
    dec_avg = models.FloatField(verbose_name="Dec Degree Average")
    ra_std = models.FloatField(verbose_name="Ra Degree Std")
    dec_std = models.FloatField(verbose_name="Dec Degree Std")
    ra_range = models.FloatField(verbose_name="Ra Range")
    dec_range = models.FloatField(verbose_name="Ra Range")
    euc = models.FloatField(verbose_name="Euclidean Distance")

    objects = SciManager()

    def __unicode__(self):
        return u"{} -> {}".format(
            unicode(self.master_src), unicode(self.pawprint_src))

    def save(self, *args, **kwargs):
        m_ra, m_dec = self.master_src.ra_k, self.master_src.dec_k
        p_ra, p_dec = self.pawprint_src.ra_deg, self.pawprint_src.dec_deg

        ras, decs = np.array([m_ra, p_ra]), np.array([m_dec, p_dec])

        self.ra_avg = np.average(ras)
        self.dec_avg = np.average(decs)
        self.ra_std = np.std(ras)
        self.dec_std = np.std(decs)
        self.ra_range = np.abs(np.subtract(*ras))
        self.dec_range = np.abs(np.subtract(*decs))
        self.euc = np.linalg.norm(np.array([m_ra, m_dec]) -
                                  np.array([p_ra, p_dec]))

        super(Match, self).save(*args, **kwargs)


#==============================================================================
# CLDO
#==============================================================================


class CldoD001Source(SaveTheChange, models.Model):

    _orig_pk = models.IntegerField(unique=True, db_column="cldo_d001_object")

    lcurves_master_source = models.OneToOneField(
        MasterSource, related_name="+", null=True, blank=True
    )

    objects = SciManager()

    @property
    def d001_object(self):
        if not hasattr(self, "__d001_object"):
            from carpyncho.cldo.models import D001Object
            self.__d001_object = D001Object.objects.get(pk=self._orig_pk)
        return self.__d001_object

    @d001_object.setter
    def d001_object(self, v):
        from carpyncho.cldo.models import D001Object
        if not isinstance(v, D001Object):
            raise TypeError("Must be D001Object instance")
        self.__d001_object = v
        self._orig_pk = v.pk

    def __unicode__(self):
        if self.lcurves_master_source:
            return u"{}->{}".format(
                self.d001_object.obj_id, self.lcurves_master_source
            )
        return unicode(self.d001_object.obj_id)


class CldoLCurvesPawprintMatch(SaveTheChange, models.Model):
    class Meta:
        unique_together = ["pawprint_source", "_d001_lc_pk"]

    cldo_d001_source = models.ForeignKey(
        CldoD001Source, related_name="matches"
    )
    _d001_lc_pk = models.IntegerField(db_column="d001_lc", unique=True)
    pawprint_source = models.OneToOneField(PawprintSource, related_name="+")
    hjd_avg = models.FloatField()
    hjd_delta_avg = models.FloatField()

    @property
    def d001_lc(self):
        if not hasattr(self, "__d001_lc"):
            from carpyncho.cldo.models import D001LC
            self.__d001_lc = D001LC.objects.get(pk=self._d001_lc_pk)
        return self.__d001_lc

    @d001_lc.setter
    def d001_lc(self, v):
        from carpyncho.cldo.models import D001LC
        if not isinstance(v, D001LC):
            raise TypeError("Must be D001LC instance")
        self.__d001_lc = v
        self._d001_lc_pk = v.pk


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
