from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class MyM2M(models.ManyToManyField):
    pass


class BugTag(TaggedItemBase):

    content_object = models.ForeignKey('Bug')
    note = models.CharField(max_length=50)


class Bug(models.Model):

    name = models.CharField(max_length=100)
    tags = TaggableManager(through=BugTag)


class X(models.Model):
    foo = models.ManyToManyField(Bug)


class Y(models.Model):
    bar = MyM2M(Bug)
