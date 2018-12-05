# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0041_auto_20150728_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersource',
            name='z',
            field=models.FloatField(default=-1, verbose_name='Z'),
            preserve_default=False,
        ),
    ]
