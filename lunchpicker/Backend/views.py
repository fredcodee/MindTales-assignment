from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer , UserSerializer





@api_view(['GET'])
def healthCheck(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in request.data]
    if missing_fields:
        # If any required fields are missing, return a custom error message
        return Response(
            {"error": "Missing information for complete registration", "missing_fields": missing_fields},
            status=status.HTTP_400_BAD_REQUEST
        )

    if serializer.is_valid():
        serializer.save()
        return Response({
            'id': serializer.data['id'],
            'username': serializer.data['username'],
            'email': serializer.data['email']
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated]) 
@api_view(['POST'])
def createRestaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# upload menu
@permission_classes([IsAuthenticated]) 
@api_view(['POST'])
def uploadMenu(request):
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all restaurants
@permission_classes([IsAuthenticated]) 
@api_view(['GET'])
def getRestaurants(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)

#get menu of a restaurant by filtered by date and restaurant id
@permission_classes([IsAuthenticated]) 
@api_view(['GET'])
def getMenu(request):
    date = request.data['date']
    restaurant_id = request.data['restaurant_id']
    print(date, restaurant_id)
    menu = Menu.objects.filter(date=date, restaurant=restaurant_id)
    serializer = MenuSerializer(menu, many=True)
    return Response(serializer.data)
    

#vote for menu
@permission_classes([IsAuthenticated]) 
@api_view(['POST'])
def vote_for_menu(request):
    version = request.headers.get('Version')  #assuming mobile versions will be sent here the old one is 1.0 and latest version is 2.0

    if version == '1.0':  # Old API version
        # Accept only one menu ID
        menu_id =  request.data['menu_id']
        points = request.data['points']
        date =  request.data['date']
        menu = Menu.objects.get(id=menu_id, date=date)
        voteVerification(menu_id, points, date)
        Vote.objects.create(user=request.user, date=date, menu=menu, points=int(points))
        return Response({"message": "Vote cast successfully"}, status=status.HTTP_201_CREATED)
    
    elif version == '2.0':  # New API version
        # Accept up to three menu IDs with respective points
        menu_votes = request.data['menu_votes']  # Expects a list of dicts like [{'menu_id': 1, 'points': 1}, ...]
        date =  request.data['date']
        
        for mv in menu_votes:
            menu = Menu.objects.get(id=mv['menu_id'])
            points = mv['points']
            voteVerification(mv['menu_id'], mv['points'], date)
        
        for mv in menu_votes:
            menu = Menu.objects.get(id=mv['menu_id'])
            points = mv['points']
            Vote.objects.create(user=request.user, date=date, menu=menu, points=int(points))

        return Response({"message": "Votes cast successfully"}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({"error": "Invalid API version"}, status=status.HTTP_400_BAD_REQUEST)


def voteVerification(menu_id, points, date):
    menu = Menu.objects.get(id=menu_id, date=date)
    points=int(points)
    if not menu:
        return Response({"error": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)
    if points < 1 or points > 3:
        return Response({"error": "Points must be between 1 and 3"}, status=status.HTTP_400_BAD_REQUEST)
    
    

#get results by date
@permission_classes([IsAuthenticated]) 
@api_view(['GET'])
def getResults(request):
    date = request.data['date']
    menu = Menu.objects.filter(date=date)
    data = []
    # get the votes for each menu
    for list in menu:
        restaurant_name = list.restaurant.name
        votes = Vote.objects.filter(date=date, menu=list)
        total_votes  = 0
        for vote in votes:
            total_votes += vote.points
        data.append({'restaurant_name': restaurant_name,'menu': list, 'total_votes': total_votes})
        
    if len(data) == 0:
        return Response({"error": "No votes found"}, status=status.HTTP_404_NOT_FOUND)
    
    data.sort(key=lambda x: x['total_votes'], reverse=True)   
    return Response({"date": date, "results": data}, status=status.HTTP_200_OK)