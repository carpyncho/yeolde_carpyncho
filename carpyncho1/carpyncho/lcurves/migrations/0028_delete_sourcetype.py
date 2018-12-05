# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0027_remove_mastersource_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SourceType',
        ),
    ]
