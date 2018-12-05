# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0004_auto_20150226_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pawprint',
            name='hjd',
        ),
        migrations.RemoveField(
            model_name='pawprintsource',
            name='mjd',
        ),
    ]
