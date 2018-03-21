#!/usr/bin/env python
# -*- coding: utf-8 -*-
import docker
import os
import subprocess
import sys
from subprocess import call

from api.tasks import *
# Get docker client
client = docker.from_env()

# Get container Object
contsList = client.containers.list()
print contsList
cont = contsList[0]

# Update container resources
print cont.id
cont_id = cont.id
memoryUpdate = 500
memoryUpdate = str(memoryUpdate)
cpuUpdate = 3
cpuUpdate = str(cpuUpdate)
#os.system("docker update -m " + memoryUpdate + "MB " + cont_id)
os.system("docker update --cpus=\'"+cpuUpdate+"\' "+ cont_id)


number = add.delay(8,2)
print(number)
# Toggle between denying/accepting requests in container ports
# subprocess.call([‘sudo’, sys.executable, ‘./ufw_cust.py’, ‘deny’, ‘8000’])


