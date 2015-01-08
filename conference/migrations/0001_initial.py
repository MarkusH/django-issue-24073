# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.manager
import conference.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudienceLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('level', models.IntegerField(null=True, verbose_name='level', blank=True)),
            ],
            options={
                'ordering': ['level'],
                'verbose_name': 'target-audience',
                'verbose_name_plural': 'target-audiences',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_objects', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(null=True, verbose_name='slug', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='end date', blank=True)),
                ('reviews_start_date', models.DateTimeField(null=True, blank=True)),
                ('reviews_end_date', models.DateTimeField(null=True, blank=True)),
                ('reviews_active', models.NullBooleanField()),
                ('tickets_editable', models.BooleanField(default=True)),
                ('tickets_editable_until', models.DateTimeField(null=True, blank=True)),
                ('anonymize_proposal_author', models.BooleanField(verbose_name='anonymize proposal author', default=True)),
            ],
            options={
                'verbose_name': 'conference',
                'verbose_name_plural': 'conferences',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('used_for_sessions', models.BooleanField(verbose_name='used for sessions', default=True)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_date', models.DateField(null=True, verbose_name='start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='end date', blank=True)),
                ('slug', models.SlugField(null=True, verbose_name='slug', blank=True)),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', related_name='sections', verbose_name='conference')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_objects', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='SessionDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name='label')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('minutes', models.IntegerField(verbose_name='minutes')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'verbose_name': 'session duration',
                'verbose_name_plural': 'session durations',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_objects', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='SessionKind',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('closed', models.NullBooleanField()),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
                ('sections', models.ManyToManyField(to='conference.Section', verbose_name='section')),
            ],
            options={
                'ordering': ('start_date', 'end_date', 'name'),
                'verbose_name': 'session type',
                'verbose_name_plural': 'session types',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_objects', conference.models.ActiveSessionKindManager()),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('visible', models.BooleanField(verbose_name='visible', default=True)),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'track',
                'verbose_name_plural': 'tracks',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_objects', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.AddField(
            model_name='audiencelevel',
            name='conference',
            field=models.ForeignKey(to='conference.Conference', verbose_name='conference'),
        ),
    ]
