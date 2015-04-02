# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b', '0002_mymodel_a'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='a',
        ),
    ]
