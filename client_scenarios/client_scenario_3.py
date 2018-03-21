#!/usr/bin/python

import time
import random
import subprocess
import datetime
import sys
import requests
import os

MINUTE = 60

def main():
    
    # initially sleep for a (uniformly) random time between 0 and 6 seconds
    # time.sleep(random.randint(0,6))

    first_start_time = time.time()

    # for the first X minutes send "not fire-containing" images
    while (time.time() - first_start_time) < 0.6*MINUTE:
        n = str(random.randint(1,3))
        img = "n"+n+".jpg"
        size = os.path.getsize("../images/"+img)
        pts = datetime.datetime.now().strftime('%s')
        json = {"size" : size, "start_time" : pts}
        subprocess.call(["curl", "-s", "-X", \
                "POST", "-F", "file=@../images/"+img+";type=image/jpeg", "http://10.0.0.50:8000/ca_tf/imageUpload/"+img])

    second_start_time = time.time()

    # for the next X minutes send "fire-containing" images
    while (time.time() - second_start_time) < 0.6*MINUTE:
        n = str(random.randint(1,9))
        img = "y"+n+".jpg"
        size = os.path.getsize("../images/"+img)
        pts = datetime.datetime.now().strftime('%s')
        json = {"size" : size, "start_time" : pts}
        subprocess.call(["curl", "-s", "-X", \
                "POST", "-F", "file=@../images/"+img+";type=image/jpeg", "http://10.0.0.50:8000/ca_tf/imageUpload/"+img])

if __name__ == "__main__":
    main()
