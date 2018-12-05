from django.db import models

class TileDim(models.Model):
    class Meta:
        app_label = "cube"
        db_table = "tile_dim"

    name = models.CharField(max_length=255, primary_key=True)


class PawprintDim(models.Model):
    class Meta:
        app_label = "cube"
        db_table = "pawprint_dim"

    name = models.CharField(max_length=255, primary_key=True)


class MagDim(models.Model):
    class Meta:
        app_label = "cube"
        db_table = "mag_dim"

    mag = models.CharField(max_length=255, primary_key=True)
    mag_err = models.CharField(max_length=255)


class MJDDim(models.Model):
    class Meta:
        app_label = "cube"
        db_table = "mjd_dim"

    mjd = models.CharField(max_length=255, primary_key=True)


class Fact(models.Model):
    class Meta:
        app_label = "cube"
        db_table = "facts"

    sk = models.PositiveIntegerField(unique=True)
    tile = models.ForeignKey(TileDim)
    pawprint = models.ForeignKey(PawprintDim)

    mag = models.ForeignKey(MagDim)
    mjd = models.ForeignKey(MJDDim)

    ra = models.FloatField()
    dec = models.FloatField()

    cnt = models.PositiveIntegerField(default=1)




