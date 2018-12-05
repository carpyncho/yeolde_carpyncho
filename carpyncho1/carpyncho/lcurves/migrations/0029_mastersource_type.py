# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0028_delete_sourcetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersource',
            name='type',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Name', choices=[(b'RRab', b'RR Lyrae ab type'), (b'RRc', b'RR Lyrae c type')]),
            preserve_default=True,
        ),
    ]
