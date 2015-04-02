# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0001_initial'),
        ('b', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='a',
            field=models.ForeignKey(null=True, to='a.MyModel'),
        ),
    ]
