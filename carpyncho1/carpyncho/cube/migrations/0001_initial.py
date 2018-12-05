# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sk', models.PositiveIntegerField(unique=True)),
                ('ra', models.FloatField()),
                ('dec', models.FloatField()),
                ('cnt', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'facts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MagDim',
            fields=[
                ('mag', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('mag_err', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'mag_dim',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MJDDim',
            fields=[
                ('mjd', models.CharField(max_length=255, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'mjd_dim',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PawprintDim',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'pawprint_dim',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TileDim',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'tile_dim',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fact',
            name='mag',
            field=models.ForeignKey(to='cube.MagDim'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fact',
            name='mjd',
            field=models.ForeignKey(to='cube.MJDDim'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fact',
            name='pawprint',
            field=models.ForeignKey(to='cube.PawprintDim'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fact',
            name='tile',
            field=models.ForeignKey(to='cube.TileDim'),
            preserve_default=True,
        ),
    ]
