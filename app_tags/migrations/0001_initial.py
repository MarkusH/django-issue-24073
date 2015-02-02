# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BugTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('note', models.CharField(max_length=50)),
                ('content_object', models.ForeignKey(to='app_tags.Bug')),
                ('tag', models.ForeignKey(related_name='app_tags_bugtag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bug',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', through='app_tags.BugTag', help_text='A comma-separated list of tags.', to='taggit.Tag'),
            preserve_default=True,
        ),
    ]
