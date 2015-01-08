# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('short_info', models.TextField(verbose_name='short info', blank=True)),
                ('avatar', models.ImageField(upload_to='avatars', null=True, verbose_name='avatar', blank=True)),
                ('num_accompanying_children', models.PositiveIntegerField(null=True, verbose_name='Number of accompanying children', default=0, blank=True)),
                ('age_accompanying_children', models.CharField(max_length=20, verbose_name='Age of accompanying children', blank=True)),
                ('twitter', models.CharField(max_length=20, verbose_name='Twitter', blank=True)),
                ('website', models.URLField(verbose_name='Website', blank=True)),
                ('organisation', models.TextField(verbose_name='Organisation', blank=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='Full name', blank=True)),
                ('display_name', models.CharField(help_text='What name should be displayed to other people?', verbose_name='Display name', max_length=255, blank=True)),
                ('addressed_as', models.CharField(help_text='How should we call you in mails and dialogs throughout the website?', verbose_name='Address me as', max_length=255, blank=True)),
                ('accept_pysv_conferences', models.BooleanField(verbose_name='Allow copying to PySV conferences', default=False)),
                ('accept_ep_conferences', models.BooleanField(verbose_name='Allow copying to EPS conferences', default=False)),
                ('accept_job_offers', models.BooleanField(verbose_name='Allow sponsors to send job offers', default=False)),
                ('badge_status', models.ManyToManyField(to='accounts.BadgeStatus', verbose_name='Badge status', related_name='profiles', blank=True)),
                ('sessions_attending', models.ManyToManyField(to='schedule.Session', verbose_name='Trainings', related_name='attendees', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'permissions': (('send_user_mails', 'Allow sending mails to users through the website'), ('export_guidebook', 'Allow export of guidebook data'), ('see_checkin_info', 'Allow seeing check-in information'), ('perform_purchase', 'Allow performing purchases')),
            },
        ),
    ]
