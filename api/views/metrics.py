from __future__ import division
import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Tasks_Interval


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
    data = {"requests_submitted": submitted, "requests_finished": finished, "requests_rejected": rejected,
            "average_response_time": average_response_time}
    data_d = json.dumps(data)
    json_data = json.loads(data_d)

    # print(json_data)
    Tasks_Interval.objects.all().delete()
    return Response(json_data)

