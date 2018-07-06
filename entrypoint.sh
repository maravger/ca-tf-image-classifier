#!/bin/bash

python manage.py migrate
python manage.py loaddata fixtures/Tasks_Interval.json

#iperf3 -s -p 5202 -J --logfile ./log1.txt &
python -u ./manage.py runserver 0.0.0.0:8000 


