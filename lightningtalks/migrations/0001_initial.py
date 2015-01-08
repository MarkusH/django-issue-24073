# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightningTalk',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slides_url', models.URLField(null=True, verbose_name='slides URL', blank=True)),
                ('speakers', models.ManyToManyField(to='speakers.Speaker', verbose_name='speakers', related_name='lightning_talks', blank=True)),
            ],
        ),
    ]
