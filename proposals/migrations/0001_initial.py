# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import conference.models
import django.db.models.manager
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
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
                ('additional_speakers', models.ManyToManyField(to='speakers.Speaker', verbose_name='additional speakers', related_name='proposal_participations', blank=True)),
                ('audience_level', models.ForeignKey(to='conference.AudienceLevel', on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience')),
            ],
            options={
                'ordering': ['-pk'],
                'permissions': (('see_proposal_author', 'Can always see the proposal author'),),
                'verbose_name': 'proposal',
                'verbose_name_plural': 'proposals',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('slot', models.IntegerField(verbose_name='timeslot', choices=[(1, 'morning'), (2, 'afternoon')])),
                ('section', models.ForeignKey(to='conference.Section', verbose_name='section')),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'timeslot',
                'verbose_name_plural': 'timeslots',
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='available_timeslots',
            field=models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='conference',
            field=models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, verbose_name='conference'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='duration',
            field=models.ForeignKey(to='conference.SessionDuration', on_delete=django.db.models.deletion.PROTECT, verbose_name='duration'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='kind',
            field=models.ForeignKey(to='conference.SessionKind', on_delete=django.db.models.deletion.PROTECT, verbose_name='type'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='speaker',
            field=models.ForeignKey(to='speakers.Speaker', on_delete=django.db.models.deletion.PROTECT, related_name='proposals', verbose_name='speaker'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='track',
            field=models.ForeignKey(to='conference.Track', verbose_name='track', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('date', 'slot', 'section')]),
        ),
    ]
