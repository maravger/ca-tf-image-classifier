# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Tasks_Interval(models.Model):
    number_to_accept = models.IntegerField()
    submitted = models.IntegerField()
    finished = models.IntegerField()
    rejected = models.IntegerField()
    total_time = models.FloatField()
