# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-07 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180507_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks_interval',
            name='number_to_accept',
            field=models.IntegerField(default=10000000),
        ),
    ]