# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0003_pawprintsource_hjd'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawprint',
            name='hjd',
            field=models.FloatField(default=None, null=True, verbose_name='HJD'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pawprint',
            name='mjd',
            field=models.FloatField(default=None, null=True, verbose_name='MJD'),
            preserve_default=True,
        ),
    ]
