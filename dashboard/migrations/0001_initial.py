# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard_status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('up', models.IntegerField(null=True, blank=True)),
                ('down', models.IntegerField(null=True, blank=True)),
                ('accepted', models.IntegerField(null=True, blank=True)),
                ('unaccepted', models.IntegerField(null=True, blank=True)),
                ('rejected', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dashboard_status',
            },
        ),
    ]
