from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer

# Create your views here.

@api_view(['GET'])
def healthCheck(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': 'heath/',
            'method': 'GET',
            'body': None,
            'description': 'Returns backeand server status'
        }
    ]

    return Response(routes)

# user registration
# user login
# create resturants
# upload menu
# vote on menu