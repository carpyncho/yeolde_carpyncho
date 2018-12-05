# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0043_auto_20150729_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cldolcurvespawprintmatch',
            name='pawprint_source',
            field=models.OneToOneField(related_name='+', to='lcurves.PawprintSource'),
        ),
        migrations.AlterField(
            model_name='mastersource',
            name='type',
            field=models.CharField(default=None, choices=[(b'RRLyrae AB', b'RRLyrae AB'), (b'RRLyrae C', b'RRLyrae C')], max_length=255, help_text='This identify the source type', null=True, verbose_name='Type'),
        ),
    ]
