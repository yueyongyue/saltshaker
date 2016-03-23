# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minions', '0002_minions_status_minion_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minions_status',
            name='minion_config',
            field=models.BooleanField(default=False),
        ),
    ]
