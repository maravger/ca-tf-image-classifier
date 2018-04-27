
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import RequestToAccept

@api_view(['POST'])
@permission_classes((AllowAny, ))    

def post (request, format = None):
    
    number_to_accept = request.data['number']

    RequestToAccept.objects.all().delete()
    b = RequestToAccept(number_to_accept=number_to_accept, count=0)
    b.save()

    all_entries = RequestToAccept.objects.all()
    for e in all_entries:
        print(e.number_to_accept)
        print(e.count)

    return Response(status=status.HTTP_201_CREATED)     

