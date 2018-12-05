# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0036_auto_20150430_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightcurve',
            name='recalc',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
