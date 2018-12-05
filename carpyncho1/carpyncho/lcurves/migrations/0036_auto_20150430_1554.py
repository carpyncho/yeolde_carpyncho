# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0035_auto_20150430_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lightcurve',
            name='gls_freq',
            field=models.FloatField(default=None, null=True, verbose_name='GLS Frequency'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lightcurve',
            name='pdm_freq',
            field=models.FloatField(default=None, null=True, verbose_name='PDM Frequency'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lightcurve',
            name='pdm_period',
            field=models.FloatField(default=None, null=True, verbose_name='PDM Period'),
            preserve_default=True,
        ),
    ]
