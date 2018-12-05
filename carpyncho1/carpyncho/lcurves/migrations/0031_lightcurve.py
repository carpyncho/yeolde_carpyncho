# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0030_auto_20150428_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightCurve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obs_number', models.IntegerField(verbose_name=b'Number of Observations')),
                ('pdm', models.FloatField(verbose_name='PDM')),
                ('gls', models.FloatField(verbose_name='GLS')),
                ('source', models.OneToOneField(related_name='+', to='lcurves.MasterSource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
