# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0015_auto_20150317_1825'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cldolcurvespawprintmatch',
            unique_together=set([('pawprint_source', '_d001_lc_pk')]),
        ),
    ]
