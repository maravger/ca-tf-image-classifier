#!/bin/bash

# Trap ctrl-c (INT) and call cleanup()
trap cleanup INT

function cleanup() {
    echo
	    echo "** Terminating Container and cleaning up..."
}


python manage.py migrate
python manage.py loaddata fixtures/Tasks_Interval.json
python -u ./manage.py runserver 0.0.0.0:8000