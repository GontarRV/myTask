from django.db import models
from CarPark.models import Enterprise
from django.contrib.auth.models import User
from django.db.models import AutoField


class Manager(User):
    enterprise = models.ManyToManyField(Enterprise, related_name='manager', blank=True)