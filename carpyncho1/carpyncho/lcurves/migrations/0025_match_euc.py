# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0024_auto_20150408_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='euc',
            field=models.FloatField(default=-1, verbose_name=b'Euclidean Distance'),
            preserve_default=False,
        ),
    ]
