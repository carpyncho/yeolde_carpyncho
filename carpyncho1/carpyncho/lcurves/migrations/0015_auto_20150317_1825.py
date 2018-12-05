# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0014_cldolcurvespawprintmatch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cldolcurvespawprintmatch',
            old_name='hjd_svg',
            new_name='hjd_avg',
        ),
        migrations.RenameField(
            model_name='cldolcurvespawprintmatch',
            old_name='hjd_delta',
            new_name='hjd_delta_avg',
        ),
    ]
