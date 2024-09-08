
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Topic
from .serializers import RoomSerailizer, UserSerialize
from django.contrib.auth.models import User

@api_view(['GET'])
def getRoutes(request):
    
    context = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topic',
        'GET /api/user', 




    ]

    return Response(context)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerailizer(rooms, many=True)
 
    return Response(serializer.data)




@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(pk =pk)
    # the many parameter is for multiple object, here in this case there is single object so that many is false : 

    serializer = RoomSerailizer(room, many =False)
    return Response(serializer.data)


@api_view(['GET', 'POST']) # so thi is the function decorator for creating the api  and the 'method we want the requested user can make are also mention here' 
def getTopic(request):

    somewhere = {
        'locatioin': 'India', 

    }
    return Response(somewhere)


@api_view(['GET'])
def getUser(request):

    user = User.objects.all()
    users = UserSerialize(user, many =True)
    return Response(users.data)



