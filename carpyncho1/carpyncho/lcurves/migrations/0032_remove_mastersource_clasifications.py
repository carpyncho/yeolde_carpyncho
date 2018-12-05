# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0031_lightcurve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mastersource',
            name='clasifications',
        ),
    ]
