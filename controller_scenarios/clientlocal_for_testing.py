#!/usr/bin/env python3

import time
import random
import subprocess
import datetime
import sys
import os
import requests
import subprocess
import asyncio
import concurrent.futures
import logging
from scipy.stats import poisson
from requests.exceptions import ConnectionError

MINUTE = 60

def main():
    rate = int(sys.argv[1])
    print (rate)
    first_start_time = time.time()
    interval_counter = 0
    while (time.time() - first_start_time) < 600*MINUTE:
#        subprocess.call(["iperf3", "-c", "10.0.0.50", "-p", "5202", "-u", "-R", "-t", "2", "-J"])
        
        if (time.time()- first_start_time  > interval_counter*30):
            logging.basicConfig(
                    level=logging.CRITICAL,
                    format='%(threadName)10s %(name)18s: %(message)s',
                    stream=sys.stderr,
                )
            loop = asyncio.get_event_loop()
            loop.run_until_complete(post(rate))
            interval_counter += 1

        # print(r.text)
        # subprocess.call(["curl", "-s", "-X", \
        # "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.27.181:8000/ca_tf/imageUpload/"+img])

        # time.sleep(random.randint(0,3))
        #time.sleep(sleeping_time)
        #sleeping_time = random.randint(0, sleeping_time)


async def post(rate):
        log = logging.getLogger('run_blocking_tasks')
        log.info('starting')
        log.info('creating executor tasks')
        skata = poisson.rvs(rate)
        while (skata<1) or (skata>42) or (skata<rate-5) or (skata>rate+5):
            skata = poisson.rvs(rate)
        print ("poisson number")
        print (skata)

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            loop = asyncio.get_event_loop()
            response = []
            st = []
            for i in range(skata):
                if i==0:
                    st.append(random.expovariate(0.5))
                else:
                    st.append(st[i-1] + random.expovariate(0.5))
                    if ((st[i]>29)):
                        st[i] = random.expovariate(0.5)
                    elif (st[i]>29):    
                        st.append(st[i]+random.expovariate(0.5))   
                print (st[i])
            futures = [
                loop.run_in_executor(
                    executor,
                    post_skata,
                    st[i],
                )
                for i in range(skata)
            ]
            #log.info('waiting for executor tasks')
            completed, pending = await asyncio.wait(futures)
            results = [t.result() for t in completed]
            #log.info('results: {!r}'.format(results))

            #log.info('exiting')

            #for response in await asyncio.gather(*futures):
            #    pass


def post_skata(n):
    #time.sleep(random.randint(n,n+1))
    time.sleep(n)
    log = logging.getLogger('blocks({})'.format(n))
    #log.info('running')

    n = str(random.randint(1, 3))
    img = "n" + n + ".jpg"
    p = str(random.randint(0,1))
    #post_url = "http://10.0.0.50:8000/ca_tf/imageUpload/" + img
    post_url = "http://192.168.0.1:8004/central_controller/offload/app/" + p
    size = os.path.getsize("../images/" + img)
    pts = time.time()  # * 1000
    json = {"size": size, "start_time": pts}
    files = {"file": open("../images/" + img, "rb")}
    #log.info('running')

    try:
    	r = requests.post(post_url, files=files, data=json)
    except ConnectionError as e:
        print (e)
        os.system("./fix_connection.sh")

    #log.info('done')

if __name__ == "__main__":
    main()
