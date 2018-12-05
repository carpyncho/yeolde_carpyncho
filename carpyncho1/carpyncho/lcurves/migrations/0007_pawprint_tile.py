# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0006_auto_20150304_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawprint',
            name='tile',
            field=models.ManyToManyField(related_name='pawprints', verbose_name='Tile', through='lcurves.PawprintXModel', to='lcurves.Tile'),
            preserve_default=True,
        ),
    ]
