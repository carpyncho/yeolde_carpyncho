# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0021_auto_20150320_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawprint',
            name='has_sources',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
