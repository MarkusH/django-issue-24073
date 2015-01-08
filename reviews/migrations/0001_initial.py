# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import conference.models
import reviews.models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0001_initial'),
        ('conference', '0001_initial'),
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', models.TextField(verbose_name='content')),
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
                ('deleted', models.BooleanField(verbose_name='deleted', default=False)),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='deleted at', blank=True)),
                ('deleted_reason', models.TextField(null=True, verbose_name='deletion reason', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('deleted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='deleted by', null=True, blank=True, related_name='deleted_comments')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='ProposalMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('num_comments', models.PositiveIntegerField(verbose_name='number of comments', default=0)),
                ('num_reviews', models.PositiveIntegerField(verbose_name='number of reviews', default=0)),
                ('latest_activity_date', models.DateTimeField(null=True, verbose_name='latest activity', blank=True)),
                ('latest_comment_date', models.DateTimeField(null=True, verbose_name='latest comment', blank=True)),
                ('latest_review_date', models.DateTimeField(null=True, verbose_name='latest review', blank=True)),
                ('latest_version_date', models.DateTimeField(null=True, verbose_name='latest version', blank=True)),
                ('score', models.FloatField(verbose_name='score', default=0.0)),
            ],
            options={
                'verbose_name': 'proposal metadata',
                'verbose_name_plural': 'proposal metadata',
            },
            managers=[
                ('objects', reviews.models.ProposalMetaDataManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProposalVersion',
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
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
                ('additional_speakers', models.ManyToManyField(to='speakers.Speaker', verbose_name='additional speakers', related_name='proposalversion_participations', blank=True)),
                ('audience_level', models.ForeignKey(to='conference.AudienceLevel', on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience')),
                ('available_timeslots', models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, verbose_name='conference')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('duration', models.ForeignKey(to='conference.SessionDuration', on_delete=django.db.models.deletion.PROTECT, verbose_name='duration')),
                ('kind', models.ForeignKey(to='conference.SessionKind', on_delete=django.db.models.deletion.PROTECT, verbose_name='type')),
            ],
            options={
                'verbose_name': 'proposal version',
                'verbose_name_plural': 'proposal versions',
            },
            managers=[
                ('objects', reviews.models.ProposalVersionManager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rating', models.CharField(max_length=2, verbose_name='rating', choices=[('-1', '-1'), ('-0', '-0'), ('+0', '+0'), ('+1', '+1')])),
                ('summary', models.TextField(verbose_name='summary')),
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(verbose_name='state', choices=[(0, 'pending request'), (1, 'request accepted'), (2, 'request declined')], default=0)),
                ('conference', models.ForeignKey(to='conference.Conference')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'reviewer',
                'verbose_name_plural': 'reviewers',
            },
            managers=[
                ('objects', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('proposals.proposal',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', reviews.models.ProposalsManager()),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='proposal',
            field=models.ForeignKey(to='reviews.Proposal', related_name='reviews', verbose_name='proposal'),
        ),
        migrations.AddField(
            model_name='review',
            name='proposal_version',
            field=models.ForeignKey(to='reviews.ProposalVersion', verbose_name='proposal version', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='original',
            field=models.ForeignKey(to='proposals.Proposal', related_name='versions', verbose_name='original proposal'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='speaker',
            field=models.ForeignKey(to='speakers.Speaker', on_delete=django.db.models.deletion.PROTECT, related_name='proposalversions', verbose_name='speaker'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='track',
            field=models.ForeignKey(to='conference.Track', verbose_name='track', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='latest_proposalversion',
            field=models.ForeignKey(to='reviews.ProposalVersion', verbose_name='latest proposal version', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='proposal',
            field=models.OneToOneField(to='reviews.Proposal', related_name='review_metadata', verbose_name='proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal',
            field=models.ForeignKey(to='reviews.Proposal', related_name='comments', verbose_name='proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal_version',
            field=models.ForeignKey(to='reviews.ProposalVersion', verbose_name='proposal version', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='reviewer',
            unique_together=set([('conference', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'proposal')]),
        ),
    ]
