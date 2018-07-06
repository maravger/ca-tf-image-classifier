#!/usr/bin/env python
import time
import random
import subprocess
import datetime
import sys
import requests
import os
import requests
import csv
import json
MINUTE = 60



def main():
    # initially sleep for a (uniformly) random time between 0 and 6 seconds
    # time.sleep(random.randint(0,6))

    first_start_time = time.time()
    # for the first X minutes send "not fire-containing" images
    interval_counter = 1 
    while (time.time() - first_start_time)<600*MINUTE:
        f = open("log.txt" , "a") 
        subprocess.call(["docker", "stats", "--no-stream", "--format", "{{ .MemPerc }}  {{ .CPUPerc }}"] , stdout = f) # , ">", "./log.txt"])

        if (time.time() - first_start_time) > 30* interval_counter :
            interval_counter += 1
            allNums = []
            total = 0
            mem=0 
            cpu=0
            with open('log.txt','rb') as f:
                #for line in f:
                data = f.readlines()
                for line in data:
                    allNums=[]
                    allNums += line.strip().split("%")
                    mem += float (allNums[0])
                    cpu += float (allNums[1])
                    total +=1
            r = open ('log.txt','w')
            mem_avg = round(mem/total,3)
            cpu_avg = round(cpu/total,3)

            post_url = "http://10.0.0.50:8000/ca_tf/getLogs/"
            r=requests.get(post_url)#, files=files, data=json)
            print(r.text)
            skata = json.loads(r.text)
            filename = "./statsclient"
            with open(filename, 'a') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                # If opened for the first time, insert header row
                if os.path.getsize(filename) == 0:
                    wr.writerow(["requests_submitted", "requests_finished", "requests_rejected","average_response_time", "average_transmission_time", "average_computation_time","mem_percentage","cpu_percentage"])
                wr.writerow([skata.get("requests_submitted"),skata.get("requests_finished"),skata.get("requests_rejected"),skata.get("average_response_time"),skata.get("average_transmission_time"),skata.get("average_computation_time"),mem_avg,cpu_avg])

            #time.sleep(30)
        
    

if __name__ == "__main__":
    #time.sleep(30)
    main()
