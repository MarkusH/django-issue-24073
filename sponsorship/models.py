# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conference.models import CurrentConferenceManager


class SponsorLevel(models.Model):
    conference = models.ForeignKey('conference.Conference', verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    description = models.TextField(_("description"), blank=True)
    slug = models.SlugField(_("slug"))

    objects = models.Manager()
    current_conference = CurrentConferenceManager()

    class Meta:
        ordering = ["conference", "order"]
        verbose_name = _("sponsor level")
        verbose_name_plural = _("sponsor levels")


class Sponsor(models.Model):
    name = models.CharField(_("name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    description = models.TextField(_("description"), blank=True, null=True)
    contact_name = models.CharField(_("contact_name"), max_length=100, blank=True, null=True)
    contact_email = models.EmailField(_(u"Contact e\u2011mail"), blank=True, null=True)
    logo = models.ImageField(_("logo"), upload_to="sponsor_logos/")
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    added = models.DateTimeField(_("added"))
    active = models.BooleanField(_("active"), default=False)

    custom_logo_size_listing = models.CharField(
        _("Custom logo size in listings"), max_length=9, blank=True,
        help_text=_("Format: [width]x[height]. To get the maximum height out "
                    "of a logo, use something like 300x55."),
        null=True)

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
        ordering = ['name']


class JobOffer(models.Model):
    sponsor = models.ForeignKey(Sponsor, verbose_name=_("sponsor"))
    title = models.CharField(_("Title"), max_length=255)
    text = models.TextField(_("Text"))
    link = models.URLField(_("URL"))
    active = models.BooleanField(_('Active'), default=False)

    added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('sponsor__level__order', '-added',)
        verbose_name = _('Job offer')
        verbose_name_plural = _('Job offers')
