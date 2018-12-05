# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CldoD001Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orig_pk', models.IntegerField(unique=True)),
                ('obj_id', models.IntegerField(unique=True)),
                ('ksBestAper', models.IntegerField(null=True)),
                ('ksMinMag', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('ksMaxMag', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('ksTotAmp', models.DecimalField(null=True, max_digits=4, decimal_places=3)),
                ('ksMeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=4)),
                ('ksSdevMag', models.DecimalField(null=True, max_digits=5, decimal_places=4)),
                ('ksWmeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=4)),
                ('ksWsdevMag', models.DecimalField(null=True, max_digits=5, decimal_places=4)),
                ('ksMedianMag', models.DecimalField(null=True, max_digits=6, decimal_places=4)),
                ('ksMADMag', models.DecimalField(null=True, max_digits=5, decimal_places=4)),
                ('ksMWMSSD', models.DecimalField(null=True, max_digits=6, decimal_places=4)),
                ('ksSigRat', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('nKsSucDiff', models.IntegerField(null=True)),
                ('nKsPaw', models.IntegerField(null=True)),
                ('nKsEp', models.IntegerField(null=True)),
                ('ksSkew', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('ksKurt', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('nKsOmit', models.IntegerField(null=True)),
                ('critKsSigRat', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('ratCritKsSigRat', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('ksStet', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('nKsStet', models.IntegerField(null=True)),
                ('ksStetKurt', models.DecimalField(null=True, max_digits=4, decimal_places=3)),
                ('ksStetMod', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('ksCritStet', models.DecimalField(null=True, max_digits=4, decimal_places=3)),
                ('ratKsCritStet', models.DecimalField(null=True, max_digits=5, decimal_places=3)),
                ('hWmeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('hWsdevMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('nHPaw', models.IntegerField(null=True)),
                ('hHJD', models.DecimalField(null=True, max_digits=11, decimal_places=6)),
                ('jWmeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('jWsdevMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('nJPaw', models.IntegerField(null=True)),
                ('jHJD', models.DecimalField(null=True, max_digits=11, decimal_places=6)),
                ('yWmeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('yWsdevMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('nYPaw', models.IntegerField(null=True)),
                ('yHJD', models.DecimalField(null=True, max_digits=11, decimal_places=6)),
                ('zWmeanMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('zWsdevMag', models.DecimalField(null=True, max_digits=6, decimal_places=3)),
                ('nZPaw', models.IntegerField(null=True)),
                ('zHJD', models.DecimalField(null=True, max_digits=11, decimal_places=6)),
                ('RA', models.DecimalField(null=True, max_digits=10, decimal_places=7)),
                ('DEC', models.DecimalField(null=True, max_digits=10, decimal_places=7)),
                ('GLSFreq', models.DecimalField(null=True, max_digits=7, decimal_places=6)),
                ('GLSPow', models.DecimalField(null=True, max_digits=4, decimal_places=3)),
                ('maxFreq', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
                ('nFreq', models.IntegerField(null=True)),
                ('GLSFAP', models.DecimalField(null=True, max_digits=9, decimal_places=8)),
                ('freqRes', models.DecimalField(null=True, max_digits=7, decimal_places=6)),
                ('PDMTheta', models.DecimalField(null=True, max_digits=7, decimal_places=6)),
                ('PDMFREQ', models.DecimalField(null=True, max_digits=7, decimal_places=6)),
                ('PDMFAP', models.DecimalField(null=True, max_digits=7, decimal_places=6)),
                ('lcurves_master_source', models.OneToOneField(related_name='+', null=True, blank=True, to='lcurves.MasterSource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
