#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import auth
from django.db import models


#===============================================================================
#
#===============================================================================

def upload_to(instance, filename):
    cls = type(instance)
    folder = unicode(cls._meta.verbose_name_plural)
    subfolder = "{}_{}".format(cls._meta.model_name, instance.pk)
    return "/".join([folder, subfolder, filename])


#===============================================================================
#
#===============================================================================

class Tile(models.Model):

    tile_id = models.CharField(max_length=10, unique=True)
    k_fit_fz = models.FileField(upload_to=upload_to)
    k_fit = models.FileField(upload_to=upload_to)
    j_fit_fz = models.FileField(upload_to=upload_to)
    j_fit = models.FileField(upload_to=upload_to)
    h_fit_fz = models.FileField(upload_to=upload_to)
    h_fit = models.FileField(upload_to=upload_to)
    merged_jpg = models.ImageField(upload_to=upload_to)

    def __unicode__(self):
        return u"Tile '{}'".format(self.tile_id)


class Fraction(models.Model):

    #~ k_fraction_fit = models.FileField(upload_to=upload_to)
    #~ j_fraction_fit = models.FileField(upload_to=upload_to)
    #~ h_fraction_fit = models.FileField(upload_to=upload_to)
    #~ merged_jpg = models.ImageField(upload_to=upload_to)
    tile = models.ForeignKey(Tile, related_name="fractions")

    def __unicode__(self):
        return u"Fraction of {}".format(unicode(self.tile))


class Found(models.Model):

    fraction_x_coord = models.FloatField()
    fraction_y_coord = models.FloatField()
    coord = models.TextField()
    fraction = models.ForeignKey(Fraction, related_name="founds")

    def __unicode__(self):
        return u"Candidate Found at ({}, {}) in {}".format(
            self.fraction_x_coord,
            self.fraction_y_coord,
            unicode(self.fraction)
        )



