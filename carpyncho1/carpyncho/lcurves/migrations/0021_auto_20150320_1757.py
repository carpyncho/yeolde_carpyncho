# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0020_auto_20150320_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magstats',
            name='Q',
            field=models.FloatField(null=True, verbose_name=b'Quartile Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='max',
            field=models.FloatField(null=True, verbose_name=b'Max Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='min',
            field=models.FloatField(null=True, verbose_name=b'Min Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='magstats',
            name='sum',
            field=models.FloatField(null=True, verbose_name=b'Sum'),
            preserve_default=True,
        ),
    ]
