# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0037_lightcurve_recalc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lightcurve',
            name='gls_freq',
        ),
        migrations.AddField(
            model_name='lightcurve',
            name='ls_freq',
            field=models.FloatField(default=None, null=True, verbose_name='Lomb-Scargle Frequency'),
            preserve_default=True,
        ),
    ]
