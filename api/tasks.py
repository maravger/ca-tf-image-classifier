<<<<<<< HEAD
from __future__ import absolute_import, unicode_literals
from celery import task
import os.path
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@task()
def aggregate_stats():
    print('Aggregating Interval Stats')
    cwd = os.path.dirname(__file__)

    # Calculate Interval's Submitted Requests
    with open(os.path.join(cwd, '../logs/submitted.log'), 'a+') as f:
        sub_size = sum(1 for _ in f)
    os.remove(os.path.join(cwd, '../logs/submitted.log'))

    # Calculate Interval's Finished Requests
    with open(os.path.join(cwd, '../logs/finished.log'), 'a+') as f:
        fin_size = sum(1 for _ in f)
    os.remove(os.path.join(cwd, '../logs/finished.log'))

    # Calculate Interval's Average Response Time
    with open(os.path.join(cwd, '../logs/rt.log'), 'a+') as f:
        rts = [float(a.strip()) for a in f]
    os.remove(os.path.join(cwd, '../logs/rt.log'))

    if len(rts) == 0:
        interval_art = "NaN"
    else:
        interval_art = sum(rts)/len(rts)

    # print sub_size
    # print fin_size
    logger.info('Average Interval Response Time: ' + str(interval_art))

    with open(os.path.join(cwd,'../logs/intervals.csv'), 'a') as f:
        f.write(str(str(sub_size) + ',' + str(fin_size) + ',' + str(interval_art) + '\n'))


=======
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
>>>>>>> refs/remotes/origin/master
