# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0032_remove_mastersource_clasifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasificationXMasterSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_data', picklefield.fields.PickledObjectField(editable=False)),
                ('clasification', models.ForeignKey(to='lcurves.Clasification')),
                ('master_src', models.ForeignKey(to='lcurves.MasterSource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='clasificationxmastersource',
            unique_together=set([('master_src', 'clasification')]),
        ),
        migrations.AddField(
            model_name='mastersource',
            name='clasifications',
            field=models.ManyToManyField(help_text='Identify diferents clasifications of the same source for internal propuses', related_name='sources', verbose_name=b'Clasifications', through='lcurves.ClasificationXMasterSource', to='lcurves.Clasification'),
            preserve_default=True,
        ),
    ]
