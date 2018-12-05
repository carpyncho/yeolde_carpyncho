# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0012_auto_20150311_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cldod001source',
            name='_orig_pk',
            field=models.IntegerField(unique=True, db_column=b'cldo_d001_object'),
            preserve_default=True,
        ),
    ]
