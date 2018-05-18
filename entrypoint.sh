#!/bin/bash

python manage.py migrate
python manage.py loaddata fixtures/Tasks_Interval.json

python -u ./manage.py runserver 0.0.0.0:8000
iperf3 -s -J --logfile log1.txt
