from django.db import models
from django.utils.translation import ugettext_lazy


class A(models.Model):
    x = models.IntegerField(ugettext_lazy('Menge'))
