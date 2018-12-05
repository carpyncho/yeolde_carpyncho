# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0018_magstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='magstats',
            name='obs_number',
            field=models.IntegerField(default=None, verbose_name=b'Number of Observations'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='kurtosis_test_p_value',
            field=models.FloatField(null=True, verbose_name=b'Kurtosis Test P-Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='kurtosis_test_z_score',
            field=models.FloatField(null=True, verbose_name=b'Kurtosis Test Z-Score'),
            preserve_default=True,
        ),
    ]
