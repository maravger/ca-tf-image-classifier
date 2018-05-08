#!/usr/bin/python

import time
import random
import subprocess
import datetime
import sys
import requests
import os

MINUTE = 60
GPSX = 38.3029
GPSY = 23.7535

def posttoorion(sensorid, field_score, fire_score, native_exec_time, gps1, gps2):
    pts = datetime.datetime.now().strftime('%s')

    url = 'http://193.190.127.181:1026/v2/entities'
    headers = {'Accept': 'application/json', 'X-Auth-Token': 'QGIrJsK6sSyKfvZvnsza6DlgjSUa8t'}

    json = {
        "id": sensorid,
        "type": "Raspberry_Pi",
        "nodeid": {
            "value": sensorid,
            "type": "id"
        },
        "timestamp": {
            "value": str(pts),
            "type": "time"
        },
        "fire_score": {
            "value": fire_score,
            "type": "tensorflow_score"
        },
        "field_score": {
            "value": field_score,
            "type": "tensorflow_score"
        },
        "duration": {
            "value": native_exec_time,
            "type": "seconds"
        },
        "gpsx": {
            "value": gps1,
            "type": "gps"
        },
        "gpsy": {
            "value": gps2,
            "type": "gps"
        }
    }

    json_bytes = sys.getsizeof(json)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    
    # log network traffic (naive)
    print json_bytes,headers_bytes, total
    
    size = { "size": { "value": total, "type": "bytes" } }
    json.update(size)
    response = requests.post(url, headers=headers, json=json)
    print(str(response))
    return response

def main():
    
    # initially sleep for a (uniformly) random time between 0 and 6 seconds
    # time.sleep(random.randint(0,6))

    first_start_time = time.time()

    # for the first 5 minute send "not fire-containing" images
    while (time.time() - first_start_time) < 5*MINUTE:
        pts = datetime.datetime.now().strftime('%s')
        n = str(random.randint(1,3))
        img = "../images/n"+n+".jpg"
        # fire_score = subprocess.check_output(["curl", "-s", "-X", \
        #        "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.127.181:8000/ca_tf/imageUpload/"+img])
        subprocess_log_start_time = time.time()
        fire_score = subprocess.check_output(["python", "../classify.py", img])
        subprocess_log_total_time = time.time() - subprocess_log_start_time
        posttoorion("mbp"+str(pts), 1-float(fire_score), float(fire_score), subprocess_log_total_time, GPSX, GPSY) # Post to OCB

    second_start_time = time.time()

    # for the next 5 minutes send "fire-containing" images
    while (time.time() - second_start_time) < 5*MINUTE:
        pts = datetime.datetime.now().strftime('%s')
        n = str(random.randint(1,9))
        img = "../images/y"+n+".jpg"
        #fire_score = subprocess.check_output(["curl", "-s", "-X", \
        #        "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.127.181:8000/ca_tf/imageUpload/"+img])
        subprocess_log_start_time = time.time()
        fire_score = subprocess.check_output(["python", "../classify.py", img])
        subprocess_log_total_time = time.time() - subprocess_log_start_time
        posttoorion("mbp"+str(pts), 1-float(fire_score), float(fire_score), subprocess_log_total_time, GPSX, GPSY) # Post to OCB

if __name__ == "__main__":
    main()
