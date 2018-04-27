#!/usr/bin/env python
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
    post_url = "http://127.0.0.1:8000/ca_tf/serverInfo/"
    number= 10
    pts = time.time()
    data_json = {"number" : number ,"interval_time" : pts}
    r=requests.post(post_url , json= data_json)
    print(r.text)
        #subprocess.call(["curl", "-s", "-X", \
        #        "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.127.181:8000/ca_tf/imageUpload/"+img])
        #time.sleep(random.randint(0,6))
    
        
    

if __name__ == "__main__":
    main()
