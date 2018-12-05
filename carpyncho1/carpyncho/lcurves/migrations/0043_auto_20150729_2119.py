# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0042_mastersource_z'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastersource',
            name='type',
            field=models.CharField(default=None, choices=[(b'RRLyrae A', b'RRLyrae A'), (b'RRLyrae B', b'RRLyrae B')], max_length=255, help_text='This identify the source type', null=True, verbose_name='Type'),
            preserve_default=True,
        ),
    ]
