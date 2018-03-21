#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

  
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
"celery -A ca_tf worker --app=ca_tf.celery_app:app --loglevel=info"

