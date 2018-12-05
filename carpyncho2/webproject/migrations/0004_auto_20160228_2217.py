# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-28 22:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webproject', '0003_auto_20160225_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(help_text=b'foo', max_length=500)),
                ('note', models.TextField(help_text=b'foo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='cqlast',
            options={'verbose_name': 'CQL AST', 'verbose_name_plural': 'CQL ASTs'},
        ),
        migrations.AlterModelOptions(
            name='cqlquery',
            options={'verbose_name': 'CQL Query', 'verbose_name_plural': 'CQL Queries'},
        ),
        migrations.AlterField(
            model_name='cqlquery',
            name='counter',
            field=models.PositiveIntegerField(default=0),
        ),
    ]