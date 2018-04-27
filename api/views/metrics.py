from __future__ import division
import json
from rest_framework.decorators import permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *


@api_view(['GET'])
@permission_classes((AllowAny,))

def GetLogs(request, format=None):

    # Submitted
    all_entries = RequestSubmitted.objects.all()
    submitted = all_entries.count()

    # finished
    all_entries = RequestFinished.objects.all()
    finished = all_entries.count()
    sum = 0
    for e in all_entries:
        sum += e.response_time

    if sum == 0:
        average_response_time = 0
    else:
        average_response_time = sum / finished
        average_response_time = round(average_response_time, 3)

    # rejected
    all_entries = RequestRejected.objects.all()
    rejected = all_entries.count()

    # print (submitted, finished, rejected)

    data = {"requests_submitted": submitted, "requests_finished": finished, "requests_rejected": rejected,
            "average_response_time": average_response_time}
    data_d = json.dumps(data)
    json_data = json.loads(data_d)

    # print(json_data)

    RequestSubmitted.objects.all().delete()
    RequestRejected.objects.all().delete()
    RequestFinished.objects.all().delete()

    return Response(json_data)

