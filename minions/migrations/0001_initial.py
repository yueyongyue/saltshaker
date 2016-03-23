# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Minions_status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minion_id', models.CharField(max_length=128, null=True, blank=True)),
                ('minion_version', models.CharField(max_length=128, null=True, blank=True)),
                ('minion_status', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'db_table': 'minions_status',
            },
        ),
    ]
