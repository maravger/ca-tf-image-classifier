import os
import sys
import tensorflow as tf
import json
import csv
import requests
# Create your views here.
import time
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import urllib

@api_view(['POST'])
@permission_classes((AllowAny, ))    

def post (request, format = None):
    
    number_to_accept = request.data['number']
    with open ('rules.txt', 'w') as outfile:
        outfile.write((str)(number_to_accept)+'\n')
        outfile.write((str)(0)+'\n')
    outfile.close() 
    return Response(status=status.HTTP_201_CREATED)     
