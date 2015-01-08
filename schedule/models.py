# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conference.models import CurrentConferenceManager
from proposals.models import AbstractProposal as AbstractProposalModel, Proposal as ProposalModel


EVENT_ICON_CHOICES = (
    ('coffee', _('Coffee cup')),
    ('glass', _('Glass')),
    ('lightbulb-o', _('Lightbulb')),
    ('moon-o', _('Moon')),
    ('cutlery', _('Cutlery')),
)


class LocationMixin(object):
    pass


class Session(LocationMixin, AbstractProposalModel):
    start = models.DateTimeField(_("start time"), blank=True, null=True)
    end = models.DateTimeField(_("end time"), blank=True, null=True)
    section = models.ForeignKey('conference.Section', blank=True,
        null=True, verbose_name=_("section"), related_name='sessions')
    proposal = models.ForeignKey(ProposalModel, blank=True,
        null=True, related_name='session', verbose_name=_("proposal"))
    location = models.ManyToManyField('conference.Location',
        verbose_name=_("location"), blank=True)
    is_global = models.BooleanField(_("is global"), default=False)
    released = models.BooleanField(_("released"), default=False)
    slides_url = models.URLField(_("Slides URL"), blank=True, null=True)
    video_url = models.URLField(_("Video URL"), blank=True, null=True)

    max_attendees = models.PositiveSmallIntegerField(_('Max attendees'),
        null=True, blank=True)

    class Meta(object):
        verbose_name = _('session')
        verbose_name_plural = _('sessions')


class SideEvent(LocationMixin, models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    start = models.DateTimeField(_("start time"))
    end = models.DateTimeField(_("end time"))
    section = models.ForeignKey('conference.Section', blank=True,
        null=True, verbose_name=_("section"), related_name='side_events')
    location = models.ManyToManyField('conference.Location', blank=True,
        verbose_name=_("location"))
    is_global = models.BooleanField(_("is global"), default=False)
    is_pause = models.BooleanField(_("is break"), default=False)
    is_recordable = models.BooleanField(_("is recordable"), default=False)
    conference = models.ForeignKey('conference.Conference',
        verbose_name=_("conference"))
    icon = models.CharField(max_length=50, blank=True, null=True,
        verbose_name=_("icon"), choices=EVENT_ICON_CHOICES)
    video_url = models.URLField(_("Video URL"), blank=True, null=True)

    lightning_talks = models.ManyToManyField('lightningtalks.LightningTalk',
                                            blank=True)

    objects = models.Manager()
    current_conference = CurrentConferenceManager()
