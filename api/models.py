# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models


class RequestSubmitted(models.Model):
    name = models.CharField(max_length=30)
    time_arrived = models.FloatField()


class RequestRejected(models.Model):
    name = models.CharField(max_length=30)
    time_arrived = models.FloatField()


class RequestFinished(models.Model):
    name = models.CharField(max_length=30)
    time_arrived = models.FloatField()
    response_time = models.FloatField()


class RequestToAccept(models.Model):
    number_to_accept = models.IntegerField()
    count = models.IntegerField()
