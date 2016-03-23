# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='minions_status',
            name='minion_config',
            field=models.CharField(default=b'unconfig', max_length=128),
        ),
    ]
