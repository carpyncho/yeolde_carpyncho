# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0026_auto_20150427_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mastersource',
            name='type',
        ),
    ]
