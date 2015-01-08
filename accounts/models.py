# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BadgeStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(_('slug'), max_length=50)

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    short_info = models.TextField(_('short info'), blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars', null=True, blank=True)
    num_accompanying_children = models.PositiveIntegerField(_('Number of accompanying children'),
        null=True, blank=True, default=0)
    age_accompanying_children = models.CharField(_("Age of accompanying children"), blank=True, max_length=20)
    twitter = models.CharField(_("Twitter"), blank=True, max_length=20)
    website = models.URLField(_("Website"), blank=True)
    organisation = models.TextField(_('Organisation'), blank=True)
    full_name = models.CharField(_("Full name"), max_length=255, blank=True)
    display_name = models.CharField(_("Display name"), max_length=255,
        help_text=_('What name should be displayed to other people?'),
        blank=True)
    addressed_as = models.CharField(_("Address me as"), max_length=255,
        help_text=_('How should we call you in mails and dialogs throughout the website?'),
        blank=True)
    accept_pysv_conferences = models.BooleanField(_('Allow copying to PySV conferences'),
        default=False, blank=True)
    accept_ep_conferences = models.BooleanField(_('Allow copying to EPS conferences'),
        default=False, blank=True)
    accept_job_offers = models.BooleanField(_('Allow sponsors to send job offers'),
        default=False, blank=True)

    badge_status = models.ManyToManyField('accounts.BadgeStatus', blank=True,
        verbose_name=_('Badge status'), related_name='profiles')

    sessions_attending = models.ManyToManyField('schedule.Session', blank=True,
        related_name='attendees', verbose_name=_('Trainings'))

    class Meta:
        permissions = (
            ('send_user_mails', _('Allow sending mails to users through the website')),
            ('export_guidebook', _('Allow export of guidebook data')),
            ('see_checkin_info', _('Allow seeing check-in information')),
            ('perform_purchase', _('Allow performing purchases'))
        )
