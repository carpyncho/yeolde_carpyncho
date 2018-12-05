# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0033_auto_20150429_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lightcurve',
            name='gls',
        ),
        migrations.RemoveField(
            model_name='lightcurve',
            name='pdm',
        ),
        migrations.AddField(
            model_name='lightcurve',
            name='gls_freq',
            field=models.FloatField(default=None, verbose_name='GLS Frequency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lightcurve',
            name='pdm_freq',
            field=models.FloatField(default=None, verbose_name='PDM Frequency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lightcurve',
            name='pdm_period',
            field=models.FloatField(default=None, verbose_name='PDM Period'),
            preserve_default=False,
        ),
    ]
