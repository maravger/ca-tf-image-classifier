
from __future__ import absolute_import, unicode_literals
from celery import task
import os.path
import logging
from api.models import Tasks_Interval
from django.db import transaction, OperationalError

# Get an instance of a logger
logger = logging.getLogger(__name__)

@task()
#@transaction.atomic
def post_submitted(request,filename):
    while True:       # it should work withour while loop but it seems that atomic transaction misses some submitted requests. 
        with transaction.atomic():
            s = Tasks_Interval.objects.select_for_update().first()
            submitted = s.submitted
            s.submitted = submitted + 1
            try:
                s.save()
                break
            except OperationalError:
                print("DB locked: concurrency avoided")
