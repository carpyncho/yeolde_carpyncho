# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0007_pawprint_tile'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pawprintxmodel',
            unique_together=set([('tile', 'pawprint')]),
        ),
    ]
