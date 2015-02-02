# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_tags.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tags', '0002_x_y'),
    ]

    operations = [
        migrations.AddField(
            model_name='x',
            name='foo',
            field=models.ManyToManyField(to='app_tags.Bug'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='y',
            name='bar',
            field=app_tags.models.MyM2M(to='app_tags.Bug'),
            preserve_default=True,
        ),
    ]
