from django.db import models


class MyModel(models.Model):
    a = models.ForeignKey('a.MyModel', null=True)
