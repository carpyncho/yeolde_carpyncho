# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0023_auto_20150408_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pawprintxmodel',
            name='matched',
            field=models.BooleanField(default=False, verbose_name='Matched'),
            preserve_default=True,
        ),
    ]
