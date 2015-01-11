# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_c', '0002_c2'),
        ('app_b', '0002_b2'),
        ('app_a', '0002_a2'),
    ]

    operations = [
        migrations.CreateModel(
            name='A3',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('b2', models.ForeignKey(to='app_b.B2')),
                ('c2', models.ForeignKey(to='app_c.C2')),
            ],
        ),
    ]
