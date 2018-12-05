# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0040_auto_20150728_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersource',
            name='x',
            field=models.FloatField(default=-1, verbose_name='Y'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastersource',
            name='y',
            field=models.FloatField(default=-1, verbose_name='X'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pawprintsource',
            name='pwp_x',
            field=models.FloatField(verbose_name='Pawprint X'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pawprintsource',
            name='pwp_y',
            field=models.FloatField(verbose_name='Pawprint Y'),
            preserve_default=True,
        ),
    ]
