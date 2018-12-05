# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0022_pawprint_has_sources'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pawprintxmodel',
            old_name='sync',
            new_name='matched',
        ),
    ]
