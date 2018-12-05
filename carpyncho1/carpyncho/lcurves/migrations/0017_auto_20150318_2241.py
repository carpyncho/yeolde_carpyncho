# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0016_auto_20150317_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='dec_avg',
            field=models.FloatField(default=0, verbose_name=b'Dec Degree Average'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='dec_range',
            field=models.FloatField(default=0, verbose_name=b'Ra Range'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='dec_std',
            field=models.FloatField(default=0, verbose_name=b'Dec Degree Std'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='ra_avg',
            field=models.FloatField(default=0, verbose_name=b'Ra Degree Average'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='ra_range',
            field=models.FloatField(default=0, verbose_name=b'Ra Range'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='ra_std',
            field=models.FloatField(default=0, verbose_name=b'Ra Degree Std'),
            preserve_default=False,
        ),
    ]
