# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class LightningTalk(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    speakers = models.ManyToManyField(
        "speakers.Speaker", related_name='lightning_talks',
        blank=True, verbose_name=_("speakers"))
    description = models.TextField(_("description"), blank=True, null=True)
    slides_url = models.URLField(_("slides URL"), blank=True, null=True)
