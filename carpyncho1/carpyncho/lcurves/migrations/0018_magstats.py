# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0017_auto_20150318_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recalc', models.BooleanField(default=True)),
                ('avg', models.FloatField(verbose_name=b'Average')),
                ('q25', models.FloatField(verbose_name=b'25% Quartile')),
                ('median', models.FloatField(verbose_name=b'Median')),
                ('q75', models.FloatField(verbose_name=b'75% Quartile')),
                ('mode', models.FloatField(null=True, verbose_name=b'Mode')),
                ('min', models.FloatField(verbose_name=b'Min Value')),
                ('max', models.FloatField(verbose_name=b'Max Value')),
                ('sum', models.FloatField(verbose_name=b'Sum')),
                ('Q', models.FloatField(verbose_name=b'Quartile Average')),
                ('TRI', models.FloatField(verbose_name=b'Trimedian')),
                ('MID', models.FloatField(verbose_name=b'Intra Quartile Average')),
                ('var', models.FloatField(verbose_name=b'Variance')),
                ('std', models.FloatField(verbose_name=b'Std Deviation')),
                ('range', models.FloatField(verbose_name=b'Range')),
                ('MD', models.FloatField(verbose_name=b'Average Deviation')),
                ('MeD', models.FloatField(verbose_name=b'Median Deviation')),
                ('variation', models.FloatField(verbose_name=b'Variation Coeficient')),
                ('varQ', models.FloatField(verbose_name=b'Intra Quatile deviation')),
                ('Sp_pearson', models.FloatField(verbose_name=b'Pearson Asymetry')),
                ('H1_yule', models.FloatField(verbose_name=b'Yule Asymetry')),
                ('H3_kelly', models.FloatField(verbose_name=b'Kelly Asymetry')),
                ('K1_kurtosis', models.FloatField(verbose_name=b'Robust Kurtosis')),
                ('kurtosis', models.FloatField(verbose_name=b'Kurtosis')),
                ('kurtosis_test_z_score', models.FloatField(verbose_name=b'Kurtosis Test Z-Score')),
                ('kurtosis_test_p_value', models.FloatField(verbose_name=b'Kurtosis Test P-Value')),
                ('stats_from', models.OneToOneField(to='lcurves.MasterSource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
