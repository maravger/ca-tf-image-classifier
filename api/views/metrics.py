from __future__ import division
import os
import sys
import tensorflow as tf
import json
import csv
import requests

# Create your views here.
import time
from django.http import HttpResponse , JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import urllib


@api_view(['GET'])
@permission_classes((AllowAny,))
def GetLogs(request, format=None):
    try:
        k=0
        with open('temp_response.txt', 'r') as outfile:
            for i, l in enumerate(outfile):
                pass
                k = i
            if k == 0:
                finished = 0
            else :
                finished = k + 1
        outfile.close()

    except IOError as e:
         finished = 0

    try:
        with open('temp_response.txt', 'r') as outfile:
            content = outfile.readlines()
        content = [x.strip() for x in content]
        sum = 0

        for i in range(1, len(content)):
            sum += float(content[i])

    except IOError as e:
        sum = 0

    if sum == 0:
        average_response_time = 0
    else:
        average_response_time = sum/i

    average_response_time = round(average_response_time, 3)

    try:
        with open('rules.txt', 'r') as outfile:
            content = outfile.readlines()
        content = [x.strip() for x in content]
        outfile.close()
        b = content[1]
        submitted = int(b)
    except IOError as e:
        submitted = 0

    try:
        k = 0
        with open('rejected.txt', 'r') as outfile:
            for i, l in enumerate(outfile):
                pass
                k=i
            if k == 0:
                rejected = 0
            else:
                rejected = k + 1
            outfile.close()
    except IOError as e:
        rejected = 0

    print (submitted, finished, rejected)
    data = {"requests_submitted": submitted,"requests_finished":finished,"requests_rejected":rejected,"average_response_time": average_response_time}
    data_d = json.dumps(data)
    json_data = json.loads(data_d)
    print(json_data)

    open('temp_response.txt', 'w').close()
    open('rejected.txt', 'w').close()

    return Response(json_data)
