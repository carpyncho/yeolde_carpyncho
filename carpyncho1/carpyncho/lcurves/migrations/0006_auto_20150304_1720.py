# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0005_auto_20150226_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='PawprintXModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sync', models.BooleanField(default=False, verbose_name='Sync')),
                ('pawprint', models.ForeignKey(to='lcurves.Pawprint')),
                ('tile', models.ForeignKey(to='lcurves.Tile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='pawprint',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pawprint',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='pawprint',
            name='sync',
        ),
        migrations.RemoveField(
            model_name='pawprint',
            name='tile',
        ),
    ]
