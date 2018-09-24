# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Tasks_Interval(models.Model):
    number_to_accept = models.IntegerField(default=10000000)
    submitted = models.IntegerField(default=0)
    finished = models.IntegerField(default=0)
    rejected = models.IntegerField(default=0)
    total_time = models.FloatField(default=0)
    transmission_time = models.FloatField(default=0)
    computation_time = models.FloatField(default=0)
