# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0008_auto_20150304_2053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cldod001source',
            old_name='orig_pk',
            new_name='_orig_pk',
        ),
    ]
