
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Tasks_Interval

@api_view(['POST'])
@permission_classes((AllowAny, ))    

def post (request, format = None):
    
    number_to_accept = request.data['number']

    Tasks_Interval.objects.all().delete()

    b = Tasks_Interval(number_to_accept=number_to_accept,
                       submitted=0,
                       finished=0,
                       rejected=0,
                       total_time=0)
    b.save()

    # for debugging
    # all_entries = Tasks_Interval.objects.all()
    # for e in all_entries:
    #    print(e.number_to_accept)

    return Response(status=status.HTTP_201_CREATED)     

