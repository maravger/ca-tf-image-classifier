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

    with open('temp_response.txt', 'r') as outfile:
        for i, l in enumerate(outfile):
            pass
    outfile.close()

    with open('temp_response.txt', 'r') as outfile:
        content = outfile.readlines()
    content = [x.strip() for x in content]
    finished=i+1

    sum=0
    for i in range (1 , len(content)):
        sum+= float(content[i])

    average_response_time=sum/i
    average_response_time= round(average_response_time, 3)


    with open('rejected.txt', 'r') as outfile:
        for i, l in enumerate(outfile):
            pass
    outfile.close()
    rejected=i+1

    with open('rules.txt', 'r') as outfile:
        content = outfile.readlines()
    content = [x.strip() for x in content]
    outfile.close()
    b = content[1]
    submitted = int(b)


    print (submitted,finished,rejected)
    data = {"requests_submitted": submitted,"requests_finished":finished,"requests_rejected":rejected,"average_response_time": average_response_time}
    data_d = json.dumps(data)
    json_data = json.loads(data_d)
    print(json_data)
    return Response(json_data)
