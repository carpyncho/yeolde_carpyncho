# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0038_auto_20150620_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lightcurve',
            name='ls_freq',
        ),
        migrations.RemoveField(
            model_name='lightcurve',
            name='pdm_freq',
        ),
        migrations.AddField(
            model_name='lightcurve',
            name='ls_period',
            field=models.FloatField(default=None, null=True, verbose_name='Lomb-Scargle Period'),
            preserve_default=True,
        ),
    ]
