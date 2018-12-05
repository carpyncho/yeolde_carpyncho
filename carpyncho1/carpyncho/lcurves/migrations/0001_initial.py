# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import carpyncho.lcurves.models
import carpyncho.utils.storages


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(verbose_name='Order')),
                ('ra_h', models.FloatField(verbose_name='RA H')),
                ('dec_h', models.FloatField(verbose_name='Dec H')),
                ('ra_j', models.FloatField(verbose_name='RA J')),
                ('dec_j', models.FloatField(verbose_name='Dec J')),
                ('ra_k', models.FloatField(verbose_name='RA K')),
                ('dec_k', models.FloatField(verbose_name='Dec K')),
            ],
            options={
                'verbose_name': 'Master Source',
                'verbose_name_plural': 'Masters Sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('master_src', models.ForeignKey(related_name='matches', verbose_name='Pawprint Source', to='lcurves.MasterSource')),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matchs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pawprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=carpyncho.lcurves.models.pwprints_upload, storage=carpyncho.utils.storages.OverwriteStorage(), verbose_name='File')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('sync', models.BooleanField(default=False, verbose_name='Sync')),
            ],
            options={
                'verbose_name': 'Pawprint',
                'verbose_name_plural': 'Pawprints',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PawprintSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(verbose_name='Order')),
                ('ra_deg', models.FloatField(verbose_name='RA Deg')),
                ('ra_h', models.IntegerField(verbose_name='RA H')),
                ('ra_m', models.IntegerField(verbose_name='RA m')),
                ('ra_s', models.FloatField(verbose_name='RA s')),
                ('dec_deg', models.FloatField(verbose_name='Dec Deg')),
                ('dec_d', models.IntegerField(verbose_name='Dec D')),
                ('dec_m', models.IntegerField(verbose_name='Dec m')),
                ('dec_s', models.FloatField(verbose_name='Dec s')),
                ('x', models.FloatField(verbose_name='X')),
                ('y', models.FloatField(verbose_name='Y')),
                ('mag', models.FloatField(verbose_name='Mag')),
                ('mag_err', models.FloatField(verbose_name='Mag Err')),
                ('chip_nro', models.IntegerField(verbose_name='Chip Nro')),
                ('stel_cls', models.IntegerField(verbose_name='Stellar Class')),
                ('elip', models.FloatField(verbose_name='Elip')),
                ('pos_ang', models.FloatField(verbose_name='Pos. Ang.')),
                ('mjd', models.FloatField(default=None, null=True, verbose_name='MJD')),
                ('pawprint', models.ForeignKey(related_name='sources', verbose_name='Pawprint', to='lcurves.Pawprint')),
            ],
            options={
                'verbose_name': 'Pawprint Source',
                'verbose_name_plural': 'Pawprints Sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=carpyncho.lcurves.models.masters_upload, storage=carpyncho.utils.storages.OverwriteStorage(), verbose_name='File')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Tile',
                'verbose_name_plural': 'Tile',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pawprintsource',
            unique_together=set([('pawprint', 'order')]),
        ),
        migrations.AddField(
            model_name='pawprint',
            name='tile',
            field=models.ForeignKey(related_name='pawprints', verbose_name='Tile', to='lcurves.Tile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pawprint',
            unique_together=set([('tile', 'name')]),
        ),
        migrations.AddField(
            model_name='match',
            name='pawprint_src',
            field=models.ForeignKey(related_name='matches', verbose_name='Master Source', to='lcurves.PawprintSource'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together=set([('master_src', 'pawprint_src')]),
        ),
        migrations.AddField(
            model_name='mastersource',
            name='tile',
            field=models.ForeignKey(related_name='sources', verbose_name='Tile', to='lcurves.Tile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='mastersource',
            unique_together=set([('tile', 'order')]),
        ),
    ]
