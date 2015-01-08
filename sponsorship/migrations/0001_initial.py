# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.manager
import conference.models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('link', models.URLField(verbose_name='URL')),
                ('active', models.BooleanField(verbose_name='Active', default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('sponsor__level__order', '-added'),
                'verbose_name': 'Job offer',
                'verbose_name_plural': 'Job offers',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('external_url', models.URLField(verbose_name='external URL')),
                ('annotation', models.TextField(verbose_name='annotation', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('contact_name', models.CharField(null=True, verbose_name='contact_name', max_length=100, blank=True)),
                ('contact_email', models.EmailField(null=True, verbose_name='Contact e‑mail', max_length=254, blank=True)),
                ('logo', models.ImageField(upload_to='sponsor_logos/', verbose_name='logo')),
                ('added', models.DateTimeField(verbose_name='added')),
                ('active', models.BooleanField(verbose_name='active', default=False)),
                ('custom_logo_size_listing', models.CharField(help_text='Format: [width]x[height]. To get the maximum height out of a logo, use something like 300x55.', null=True, verbose_name='Custom logo size in listings', max_length=9, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'sponsor',
                'verbose_name_plural': 'sponsors',
            },
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(verbose_name='slug')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'ordering': ['conference', 'order'],
                'verbose_name': 'sponsor level',
                'verbose_name_plural': 'sponsor levels',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_conference', conference.models.CurrentConferenceManager()),
            ],
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(to='sponsorship.SponsorLevel', verbose_name='level'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='sponsor',
            field=models.ForeignKey(to='sponsorship.Sponsor', verbose_name='sponsor'),
        ),
    ]
