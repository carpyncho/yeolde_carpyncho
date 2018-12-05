# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0019_auto_20150320_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magstats',
            name='H1_yule',
            field=models.FloatField(null=True, verbose_name=b'Yule Asymetry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='H3_kelly',
            field=models.FloatField(null=True, verbose_name=b'Kelly Asymetry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='K1_kurtosis',
            field=models.FloatField(null=True, verbose_name=b'Robust Kurtosis'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='MD',
            field=models.FloatField(null=True, verbose_name=b'Average Deviation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='MID',
            field=models.FloatField(null=True, verbose_name=b'Intra Quartile Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='MeD',
            field=models.FloatField(null=True, verbose_name=b'Median Deviation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='Sp_pearson',
            field=models.FloatField(null=True, verbose_name=b'Pearson Asymetry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='TRI',
            field=models.FloatField(null=True, verbose_name=b'Trimedian'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='avg',
            field=models.FloatField(null=True, verbose_name=b'Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='kurtosis',
            field=models.FloatField(null=True, verbose_name=b'Kurtosis'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='median',
            field=models.FloatField(null=True, verbose_name=b'Median'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='q25',
            field=models.FloatField(null=True, verbose_name=b'25% Quartile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='q75',
            field=models.FloatField(null=True, verbose_name=b'75% Quartile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='range',
            field=models.FloatField(null=True, verbose_name=b'Range'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='std',
            field=models.FloatField(null=True, verbose_name=b'Std Deviation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='var',
            field=models.FloatField(null=True, verbose_name=b'Variance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='varQ',
            field=models.FloatField(null=True, verbose_name=b'Intra Quatile deviation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='variation',
            field=models.FloatField(null=True, verbose_name=b'Variation Coeficient'),
            preserve_default=True,
        ),
    ]
