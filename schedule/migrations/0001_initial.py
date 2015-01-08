# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import conference.models
import schedule.models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('lightningtalks', '0001_initial'),
        ('conference', '0001_initial'),
        ('proposals', '0001_initial'),
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=400, verbose_name='description')),
                ('abstract', models.TextField(verbose_name='abstract')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('submission_date', models.DateTimeField(verbose_name='submission date', editable=False)),
                ('modified_date', models.DateTimeField(null=True, verbose_name='modification date', blank=True)),
                ('language', models.CharField(max_length=5, verbose_name='language', choices=[('de', 'German'), ('en', 'English')], default='de')),
                ('accept_recording', models.BooleanField(default=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start time', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end time', blank=True)),
                ('is_global', models.BooleanField(verbose_name='is global', default=False)),
                ('released', models.BooleanField(verbose_name='released', default=False)),
                ('slides_url', models.URLField(null=True, verbose_name='Slides URL', blank=True)),
                ('video_url', models.URLField(null=True, verbose_name='Video URL', blank=True)),
                ('max_attendees', models.PositiveSmallIntegerField(null=True, verbose_name='Max attendees', blank=True)),
                ('additional_speakers', models.ManyToManyField(to='speakers.Speaker', verbose_name='additional speakers', related_name='session_participations', blank=True)),
                ('audience_level', models.ForeignKey(to='conference.AudienceLevel', on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience')),
                ('available_timeslots', models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, verbose_name='conference')),
                ('duration', models.ForeignKey(to='conference.SessionDuration', on_delete=django.db.models.deletion.PROTECT, verbose_name='duration')),
                ('kind', models.ForeignKey(to='conference.SessionKind', on_delete=django.db.models.deletion.PROTECT, verbose_name='type')),
                ('location', models.ManyToManyField(to='conference.Location', verbose_name='location', blank=True)),
                ('proposal', models.ForeignKey(to='proposals.Proposal', verbose_name='proposal', null=True, blank=True, related_name='session')),
                ('section', models.ForeignKey(to='conference.Section', verbose_name='section', null=True, blank=True, related_name='sessions')),
                ('speaker', models.ForeignKey(to='speakers.Speaker', on_delete=django.db.models.deletion.PROTECT, related_name='sessions', verbose_name='speaker')),
                ('track', models.ForeignKey(to='conference.Track', verbose_name='track', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
            },
            bases=(schedule.models.LocationMixin, models.Model),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='SideEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('start', models.DateTimeField(verbose_name='start time')),
                ('end', models.DateTimeField(verbose_name='end time')),
                ('is_global', models.BooleanField(verbose_name='is global', default=False)),
                ('is_pause', models.BooleanField(verbose_name='is break', default=False)),
                ('is_recordable', models.BooleanField(verbose_name='is recordable', default=False)),
                ('icon', models.CharField(null=True, verbose_name='icon', max_length=50, choices=[('coffee', 'Coffee cup'), ('glass', 'Glass'), ('lightbulb-o', 'Lightbulb'), ('moon-o', 'Moon'), ('cutlery', 'Cutlery')], blank=True)),
                ('video_url', models.URLField(null=True, verbose_name='Video URL', blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
                ('lightning_talks', models.ManyToManyField(to='lightningtalks.LightningTalk', blank=True)),
                ('location', models.ManyToManyField(to='conference.Location', verbose_name='location', blank=True)),
                ('section', models.ForeignKey(to='conference.Section', verbose_name='section', null=True, blank=True, related_name='side_events')),
            ],
            bases=(schedule.models.LocationMixin, models.Model),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
    ]
