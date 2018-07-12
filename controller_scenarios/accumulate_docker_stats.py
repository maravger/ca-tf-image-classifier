#!/usr/bin/env python
import time
import subprocess
import os
import csv
MINUTE = 60

def main ():
    first_start_time = time.time()
    interval_counter = 1 
    while (time.time() - first_start_time)<600*MINUTE:
        f = open("log.txt" , "a") 
        subprocess.call(["docker", "stats", "--no-stream", "--format", "{{ .MemPerc }}  {{ .CPUPerc }}"] , stdout = f) # , ">", "./log.txt"])

        time.sleep(0.1)
        
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
		    if (mem>5) and (cpu>30):
                    	mem += float (allNums[0])
                    	cpu += float (allNums[1])
                    	total +=1
            r = open ('log.txt','w')
            mem_avg = round(mem/total,3)
            cpu_avg = round(cpu/total,3)
            with open('logfinal.txt','a') as mf:
                wr = csv.writer(mf, quoting=csv.QUOTE_ALL)
                if os.path.getsize('logfinal.txt') ==0:
                    wr.writerow(["mem_percentage","cpu_percentage"])
                wr.writerow([mem_avg,cpu_avg])







if __name__ == "__main__" :
    time.sleep (1)
    main()
