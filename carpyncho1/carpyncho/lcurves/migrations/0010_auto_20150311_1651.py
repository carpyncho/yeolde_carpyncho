# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0009_auto_20150311_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cldod001source',
            name='DEC',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='GLSFAP',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='GLSFreq',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='GLSPow',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='PDMFAP',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='PDMFREQ',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='PDMTheta',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='RA',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='critKsSigRat',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='freqRes',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='hHJD',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='hWmeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='hWsdevMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='jHJD',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='jWmeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='jWsdevMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksBestAper',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksCritStet',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksKurt',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMADMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMWMSSD',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMaxMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMedianMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksMinMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksSdevMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksSigRat',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksSkew',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksStet',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksStetKurt',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksStetMod',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksTotAmp',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksWmeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ksWsdevMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='maxFreq',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nFreq',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nHPaw',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nJPaw',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nKsEp',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nKsOmit',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nKsPaw',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nKsStet',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nKsSucDiff',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nYPaw',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='nZPaw',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='obj_id',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ratCritKsSigRat',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='ratKsCritStet',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='yHJD',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='yWmeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='yWsdevMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='zHJD',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='zWmeanMag',
        ),
        migrations.RemoveField(
            model_name='cldod001source',
            name='zWsdevMag',
        ),
    ]
