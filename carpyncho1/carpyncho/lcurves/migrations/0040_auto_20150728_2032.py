# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0039_auto_20150620_0036'),
    ]

    operations = [
        migrations.RenameField('pawprintsource', 'x', 'pwp_x'),
        migrations.RenameField('pawprintsource', 'y', 'pwp_y'),
    ]
