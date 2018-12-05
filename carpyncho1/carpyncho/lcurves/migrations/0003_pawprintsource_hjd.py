# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0002_cldod001source'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawprintsource',
            name='hjd',
            field=models.FloatField(default=None, null=True, verbose_name='HJD'),
            preserve_default=True,
        ),
    ]
