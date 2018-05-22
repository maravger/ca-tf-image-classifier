from __future__ import division
import json
import os
import csv
import errno
import shutil
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Tasks_Interval
from django.db import transaction


@api_view(['GET'])
@permission_classes((AllowAny,))

def GetLogs(request, format=None):
    
    # Submitted
    details = Tasks_Interval.objects.first()
    if not details:
        b = Tasks_Interval(number_to_accept=100,
                           submitted=0,
                           finished=0,
                           rejected=0,
                           total_time=0)
        b.save()
        details = Tasks_Interval.objects.first()

    submitted = details.submitted
    # finished
    finished = details.finished
    # response time
    sum = details.total_time
    if sum == 0:
        average_response_time = 0
    else:
        average_response_time = sum / finished
        average_response_time = round(average_response_time, 3)
    # rejected
    rejected = details.rejected
    # print (submitted, finished, rejected)
    # data = {"requests_submitted": submitted, "requests_finished": finished, "requests_rejected": rejected,
    #        "average_response_time": average_response_time}
    # data_d = json.dumps(data)
    # json_data = json.loads(data_d)

# temp for initial metrics
    try:
        os.makedirs("csvs")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        # Create a .csv for the interval
    filename = "csvs/stats"
    with open(filename, 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        # If opened for the first time, insert header row
        if os.path.getsize(filename) == 0:
            wr.writerow(["requests_submitted", "requests_finished", "requests_rejected",
            "average_response_time"])
        wr.writerow([submitted, finished, rejected, average_response_time])
#

    # print(json_data)
    Tasks_Interval.objects.all().delete()

    bits_per_second, jitter_ms, lost_packets, packets, lost_percent = accumulate_iperf_stats()


    
    data = {"requests_submitted": submitted, "requests_finished": finished, "requests_rejected": rejected,
            "average_response_time": average_response_time, "bits_per_second": bits_per_second,
            "jitter_ms": jitter_ms, "lost_packets": lost_packets, "packets": packets, "lost_percent": lost_percent}

    #data = {"requests_submitted": submitted, "requests_finished": finished, "requests_rejected": rejected,
     #               "average_response_time": average_response_time}

    

    data_d = json.dumps(data)
    json_data = json.loads(data_d)
    
    shutil.copyfile('./log1.txt', './loginterval.txt')
    open("./log1.txt", "w").close()
  
    return Response(json_data)


def accumulate_iperf_stats():

    a = "temp"
    r = open('log.txt', 'a+')
    with open('./log1.txt', 'rb') as f:
        for line in f:
            if a == "temp":
                r.write('[{\n')
            elif (0 <= a.find("}") < 5) and (0 <= line.find("{") < 5):
                r.write(',{')
            else:
                r.write(line)
            a = line

    r.write("]")
    r.close()

    with open('log.txt', 'r') as myfile:
        data = myfile.read().replace('\n', '')
    myfile.close()
    data = json.loads(data)
    b = []
    for each in data:
        if "end" in each:
                a = each.get("end").get("sum","skata")
                b.append(a)

    bits_per_second = 0
    jitter_ms = 0
    lost_packets = 0
    packets = 0
    lost_percent = 0
    sum = 0
    for a in b:
        sum += 1
        if "bits_per_second" in a:
            bits_per_second += a.get("bits_per_second")
        if "jitter_ms" in a:
            jitter_ms += a.get("jitter_ms")
        if "lost_packets" in a:
            lost_packets += a.get("lost_packets")
        if "packets" in a:
            packets += a.get("packets")
        if "lost_percent" in a:
            lost_percent += a.get("lost_percent")

    os.remove('log.txt')

    return bits_per_second/sum, jitter_ms/sum, lost_packets/sum, packets/sum, lost_percent/sum
