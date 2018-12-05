# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0013_auto_20150311_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='CldoLCurvesPawprintMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_d001_lc_pk', models.IntegerField(unique=True, db_column=b'd001_lc')),
                ('hjd_svg', models.FloatField()),
                ('hjd_delta', models.FloatField()),
                ('cldo_d001_source', models.ForeignKey(related_name='matches', to='lcurves.CldoD001Source')),
                ('pawprint_source', models.ForeignKey(related_name='+', to='lcurves.PawprintSource', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
