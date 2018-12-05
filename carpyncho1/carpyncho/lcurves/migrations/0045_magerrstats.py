# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0044_auto_20150810_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagErrStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recalc', models.BooleanField(default=True)),
                ('obs_number', models.IntegerField(verbose_name=b'Number of Observations')),
                ('avg', models.FloatField(null=True, verbose_name=b'Average')),
                ('q25', models.FloatField(null=True, verbose_name=b'25% Quartile')),
                ('median', models.FloatField(null=True, verbose_name=b'Median')),
                ('q75', models.FloatField(null=True, verbose_name=b'75% Quartile')),
                ('mode', models.FloatField(null=True, verbose_name=b'Mode')),
                ('min', models.FloatField(null=True, verbose_name=b'Min Value')),
                ('max', models.FloatField(null=True, verbose_name=b'Max Value')),
                ('sum', models.FloatField(null=True, verbose_name=b'Sum')),
                ('Q', models.FloatField(null=True, verbose_name=b'Quartile Average')),
                ('TRI', models.FloatField(null=True, verbose_name=b'Trimedian')),
                ('MID', models.FloatField(null=True, verbose_name=b'Intra Quartile Average')),
                ('var', models.FloatField(null=True, verbose_name=b'Variance')),
                ('std', models.FloatField(null=True, verbose_name=b'Std Deviation')),
                ('range', models.FloatField(null=True, verbose_name=b'Range')),
                ('MD', models.FloatField(null=True, verbose_name=b'Average Deviation')),
                ('MeD', models.FloatField(null=True, verbose_name=b'Median Deviation')),
                ('variation', models.FloatField(null=True, verbose_name=b'Variation Coeficient')),
                ('varQ', models.FloatField(null=True, verbose_name=b'Intra Quatile deviation')),
                ('Sp_pearson', models.FloatField(null=True, verbose_name=b'Pearson Asymetry')),
                ('H1_yule', models.FloatField(null=True, verbose_name=b'Yule Asymetry')),
                ('H3_kelly', models.FloatField(null=True, verbose_name=b'Kelly Asymetry')),
                ('K1_kurtosis', models.FloatField(null=True, verbose_name=b'Robust Kurtosis')),
                ('kurtosis', models.FloatField(null=True, verbose_name=b'Kurtosis')),
                ('kurtosis_test_z_score', models.FloatField(null=True, verbose_name=b'Kurtosis Test Z-Score')),
                ('kurtosis_test_p_value', models.FloatField(null=True, verbose_name=b'Kurtosis Test P-Value')),
                ('stats_from', models.OneToOneField(to='lcurves.MasterSource')),
            ],
        ),
    ]
