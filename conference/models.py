# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Conference(models.Model):
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), null=True, blank=True)

    # when the conference runs
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)

    reviews_start_date = models.DateTimeField(null=True, blank=True)
    reviews_end_date = models.DateTimeField(null=True, blank=True)
    reviews_active = models.NullBooleanField()

    tickets_editable = models.BooleanField(default=True)
    tickets_editable_until = models.DateTimeField(null=True, blank=True)

    anonymize_proposal_author = models.BooleanField(
        _("anonymize proposal author"), default=True)

    class Meta(object):
        verbose_name = _("conference")
        verbose_name_plural = _("conferences")


class CurrentConferenceManager(models.Manager):
    use_in_migrations = True


class Section(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"),
        related_name='sections')

    name = models.CharField(_("name"), max_length=100)

    # when the section runs
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)

    slug = models.SlugField(_("slug"), null=True, blank=True)
    order = models.IntegerField(_("order"), default=0)

    description = models.TextField(_("description"), blank=True, null=True)

    objects = models.Manager()
    current_objects = CurrentConferenceManager()

    class Meta(object):
        verbose_name = _("section")
        verbose_name_plural = _("sections")


class AudienceLevel(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"))
    level = models.IntegerField(_("level"), blank=True, null=True)

    objects = models.Manager()
    current_objects = CurrentConferenceManager()

    class Meta(object):
        verbose_name = _("target-audience")
        verbose_name_plural = _("target-audiences")
        ordering = ['level']


class SessionDuration(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    label = models.CharField(_("label"), max_length=100)
    slug = models.SlugField(_("slug"))
    minutes = models.IntegerField(_("minutes"))

    objects = models.Manager()
    current_objects = CurrentConferenceManager()

    class Meta(object):
        verbose_name = _("session duration")
        verbose_name_plural = _("session durations")


class ActiveSessionKindManager(CurrentConferenceManager):
    use_in_migrations = True


class SessionKind(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"))
    closed = models.NullBooleanField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    sections = models.ManyToManyField(Section, verbose_name=_("section"))

    # TODO: available_durations = models.ManyToManyField('SessionDuration', blank=True, null=True)
    # TODO: available_tracks = models.ManyToManyField('Track', blank=True, null=True)

    objects = models.Manager()
    current_objects = ActiveSessionKindManager()

    class Meta(object):
        ordering = ('start_date', 'end_date', 'name')
        verbose_name = _("session type")
        verbose_name_plural = _("session types")


class Track(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"))
    description = models.TextField(_("description"), blank=True, null=True)
    visible = models.BooleanField(_("visible"), default=True)
    order = models.IntegerField(_("order"), default=0)

    objects = models.Manager()
    current_objects = CurrentConferenceManager()

    class Meta(object):
        verbose_name = _("track")
        verbose_name_plural = _("tracks")
        ordering = ['order']


class Location(models.Model):
    conference = models.ForeignKey(Conference,
        verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"))
    order = models.IntegerField(_("order"), default=0)
    used_for_sessions = models.BooleanField(_("used for sessions"),
        default=True)

    objects = models.Manager()
    current_conference = CurrentConferenceManager()

    class Meta(object):
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ['order']
