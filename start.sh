#!/bin/bash

trap "kill 0" SIGINT
python ./controller_scenarios/accumulate_docker_stats.py &
docker run -it --cpuset-cpus="5,6,7" -p 8000:8000 ca-tf  
while true; do sleep 100000; done

