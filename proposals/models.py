# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conference.models import CurrentConferenceManager


DATE_SLOT_CHOICES = (
    (1, _('morning')),
    (2, _('afternoon')),
)

LANGUAGES_CHOICES = [(x[0], _(x[1])) for x in getattr(settings, 'PROPOSAL_LANGUAGES', (
    ('de', _('German')),
    ('en', _('English')),
))]


class TimeSlot(models.Model):
    date = models.DateField(_("date"))
    slot = models.IntegerField(_("timeslot"), choices=DATE_SLOT_CHOICES)
    section = models.ForeignKey('conference.Section', verbose_name=_("section"))

    class Meta(object):
        ordering = ('date',)
        unique_together = (('date', 'slot', 'section',),)
        verbose_name = _("timeslot")
        verbose_name_plural = _("timeslots")


class AbstractProposal(models.Model):
    conference = models.ForeignKey("conference.Conference",
        verbose_name="conference", on_delete=models.PROTECT)
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), max_length=400)
    abstract = models.TextField(_("abstract"))
    notes = models.TextField(_("notes"), blank=True)
    speaker = models.ForeignKey("speakers.Speaker", related_name="%(class)ss",
        verbose_name=_("speaker"), on_delete=models.PROTECT)
    additional_speakers = models.ManyToManyField("speakers.Speaker",
        blank=True, related_name="%(class)s_participations",
        verbose_name=_("additional speakers"))
    submission_date = models.DateTimeField(_("submission date"), editable=False)
    modified_date = models.DateTimeField(_("modification date"), blank=True,
        null=True)
    kind = models.ForeignKey("conference.SessionKind", verbose_name=_("type"),
        on_delete=models.PROTECT)
    audience_level = models.ForeignKey("conference.AudienceLevel",
        verbose_name=_("target-audience"), on_delete=models.PROTECT)
    duration = models.ForeignKey("conference.SessionDuration",
        verbose_name=_("duration"), on_delete=models.PROTECT)
    track = models.ForeignKey("conference.Track", verbose_name=_("track"),
        blank=True, null=True, on_delete=models.PROTECT)
    available_timeslots = models.ManyToManyField(TimeSlot,
        verbose_name=_("available timeslots"), blank=True)
    language = models.CharField(_('language'), max_length=5, blank=False,
        default=LANGUAGES_CHOICES[0][0], choices=LANGUAGES_CHOICES)
    accept_recording = models.BooleanField(default=True, blank=True)

    objects = models.Manager()
    current_conference = CurrentConferenceManager()

    class Meta(object):
        abstract = True


class Proposal(AbstractProposal):
    class Meta(object):
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")
        ordering = ['-pk']
        permissions = (
            ("see_proposal_author", _("Can always see the proposal author")),
        )
