# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lcurves', '0029_mastersource_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clasification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mastersource',
            name='clasifications',
            field=models.ManyToManyField(help_text='Identify diferents clasifications of the same source for internal propuses', related_name='sources', verbose_name=b'Clasifications', to='lcurves.Clasification'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mastersource',
            name='type',
            field=models.CharField(default=None, choices=[(b'RRab', b'RR Lyrae ab type'), (b'RRc', b'RR Lyrae c type')], max_length=255, help_text='This identify the source type', null=True, verbose_name='Type'),
            preserve_default=True,
        ),
    ]
