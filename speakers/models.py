# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class SpeakerManager(models.Manager):
    use_in_migrations = True
    use_for_related_fields = True


class Speaker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='speaker_profile')

    objects = SpeakerManager()
