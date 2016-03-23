# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import returner.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jids',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jid', models.CharField(unique=True, max_length=225, blank=True)),
                ('load', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'jids',
            },
        ),
        migrations.CreateModel(
            name='Salt_events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alter_time', returner.models.UnixTimestampField(null=True, auto_created=True)),
                ('tag', models.CharField(max_length=255, blank=True)),
                ('data', models.TextField(blank=True)),
                ('minion_id', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'salt_events',
            },
        ),
        migrations.CreateModel(
            name='Salt_grains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minion_id', models.CharField(max_length=255, null=True, blank=True)),
                ('grains', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'salt_grains',
            },
        ),
        migrations.CreateModel(
            name='Salt_returns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alter_time', returner.models.UnixTimestampField(null=True, auto_created=True)),
                ('fun', models.CharField(max_length=50, blank=True)),
                ('jid', models.CharField(max_length=255, blank=True)),
                ('returns', models.TextField(blank=True)),
                ('minion_id', models.CharField(max_length=255, blank=True)),
                ('success', models.CharField(max_length=10, blank=True)),
                ('full_ret', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'salt_returns',
            },
        ),
    ]
