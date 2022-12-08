from django.db import models
from .group import Group
from .lab import Lab

class Session(models.Model):
    group = models.ForeignKey(Group)
    lab = models.ForeignKey(Lab)