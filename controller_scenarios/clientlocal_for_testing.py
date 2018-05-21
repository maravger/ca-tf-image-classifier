#!/usr/bin/env python
import time
import random
import subprocess
import datetime
import sys
import requests
import os
import requests
import subprocess
MINUTE = 60


def main():
    requestscounter = 0
    interval_counter = 1

    sleeping_time = float(sys.argv[1])
    # initially sleep for a (uniformly) random time between 0 and 6 seconds
    # time.sleep(random.randint(0,6))

    first_start_time = time.time()

    # for the first X minutes send "not fire-containing" images
    while (time.time() - first_start_time) < 6*MINUTE:
        n = str(random.randint(1,3))
        img = "n"+n+".jpg"
        post_url = "http://10.0.0.50:8000/ca_tf/imageUpload/"+img
        size = os.path.getsize("../images/"+img)
        # pts = datetime.datetime.now().strftime('%f')
        pts = time.time()  # * 1000
        json = {"size" : size, "start_time" : pts}
        files = {"file": open("../images/"+img, "rb")}
        r = requests.post(post_url, files=files, data=json)

        requestscounter += 1
        # print(r.text)
        # subprocess.call(["curl", "-s", "-X", \
        # "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.127.181:8000/ca_tf/imageUpload/"+img])
        if (time.time() - first_start_time) / (30 * interval_counter) > 1:

            print ("request for this script this interval: %d \n" % requestscounter)
            requestscounter = 0
            interval_counter += 1

        # time.sleep(random.randint(0,3))
        time.sleep(sleeping_time)
        subprocess.call(["iperf3", "-c", "10.0.0.50", "-p", "5201", "-u", "-R", "-t", "2", "-J"])


if __name__ == "__main__":
    main()
