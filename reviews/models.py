# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conference.models import CurrentConferenceManager
from proposals.models import AbstractProposal as AbstractProposalModel, Proposal as ProposalModel

RATING_CHOICES = (
    ('-1', '-1'),
    ('-0', '-0'),
    ('+0', '+0'),
    ('+1', '+1')
)


class ProposalsManager(CurrentConferenceManager):
    use_in_migrations = True


class ProposalMetaDataManager(models.Manager):
    use_in_migrations = True


class Proposal(ProposalModel):
    objects = models.Manager()
    current_conference = ProposalsManager()

    class Meta(object):
        proxy = True


class ProposalMetaData(models.Model):
    proposal = models.OneToOneField(Proposal, verbose_name=_("proposal"),
        related_name='review_metadata')
    latest_proposalversion = models.ForeignKey("ProposalVersion",
        verbose_name=_("latest proposal version"), null=True, blank=True)
    num_comments = models.PositiveIntegerField(
        verbose_name=_("number of comments"),
        default=0)
    num_reviews = models.PositiveIntegerField(
        verbose_name=_("number of reviews"),
        default=0)
    latest_activity_date = models.DateTimeField(
        verbose_name=_("latest activity"),
        null=True, blank=True)
    latest_comment_date = models.DateTimeField(null=True, blank=True,
        verbose_name=_("latest comment"))
    latest_review_date = models.DateTimeField(null=True, blank=True,
        verbose_name=_("latest review"))
    latest_version_date = models.DateTimeField(null=True, blank=True,
        verbose_name=_("latest version"))
    score = models.FloatField(default=0.0, null=False, blank=False,
        verbose_name=_("score"))

    objects = ProposalMetaDataManager()

    class Meta(object):
        verbose_name = _("proposal metadata")
        verbose_name_plural = _("proposal metadata")


class ProposalVersionManager(models.Manager):
    use_in_migrations = True


class ProposalVersion(AbstractProposalModel):
    original = models.ForeignKey(ProposalModel,
        verbose_name=_("original proposal"),
        related_name='versions')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_("creator"))
    pub_date = models.DateTimeField(verbose_name=_("publication date"))

    objects = ProposalVersionManager()

    class Meta(object):
        verbose_name = _("proposal version")
        verbose_name_plural = _("proposal versions")


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    rating = models.CharField(choices=RATING_CHOICES, max_length=2,
        verbose_name=_("rating"))
    summary = models.TextField(verbose_name=_("summary"))
    pub_date = models.DateTimeField(verbose_name=_("publication date"))
    proposal = models.ForeignKey(Proposal, related_name="reviews",
        verbose_name=_("proposal"))
    proposal_version = models.ForeignKey(ProposalVersion, blank=True, null=True,
        verbose_name=_("proposal version"))

    class Meta(object):
        unique_together = (('user', 'proposal'),)
        verbose_name = _("review")
        verbose_name_plural = _("reviews")


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"))
    content = models.TextField(verbose_name=_("content"))
    pub_date = models.DateTimeField(verbose_name=_("publication date"))
    proposal = models.ForeignKey(Proposal, verbose_name=_("proposal"),
        related_name="comments")
    proposal_version = models.ForeignKey(ProposalVersion, blank=True, null=True,
        verbose_name=_("proposal version"))
    deleted = models.BooleanField(default=False, verbose_name=_("deleted"))
    deleted_date = models.DateTimeField(null=True, blank=True,
        verbose_name=_("deleted at"))
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
        verbose_name=_("deleted by"),
        related_name='deleted_comments')
    deleted_reason = models.TextField(blank=True, null=True,
        verbose_name=_("deletion reason"))

    class Meta(object):
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Reviewer(models.Model):

    STATE_PENDING = 0
    STATE_ACCEPTED = 1
    STATE_DECLINED = 2
    STATE_CHOICES = (
        (STATE_PENDING, _('pending request')),
        (STATE_ACCEPTED, _('request accepted')),
        (STATE_DECLINED, _('request declined')),
    )

    conference = models.ForeignKey('conference.Conference', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    state = models.PositiveSmallIntegerField(_("state"), default=STATE_PENDING, choices=STATE_CHOICES)

    objects = CurrentConferenceManager()

    class Meta:
        unique_together = (('conference', 'user'),)
        verbose_name = _('reviewer')
        verbose_name_plural = _('reviewers')
