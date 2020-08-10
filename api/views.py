from rest_framework.decorators import api_view
from rest_framework.response import Response
from management.views import *
from custom_user.models import Account, Room


# organization level apis
@api_view(['GET'])
def list_students(request):
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated and user.is_organization:
            response = listallstudents(user)
            return Response({'status': response})
        else:
            raise Exception
    except:
        return Response({"status": "forbidden"})


@api_view(['GET'])
def list_room_students(request,room_id):
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated :
            if user.is_organization or user.is_teacher:
                number=int(room_id)
                room_owner = Room.objects.get(id=number).organization
                print(room_owner)
                print(user.organization)
                if room_owner == user.organization:
                    response = listroomstudents(room_id=number)
                else:
                    response = 'unauthorized'
                return Response({'status': response})
            else:
                raise Exception
        else:
            raise Exception
    except:
        return Response({"status": "forbidden"})


@api_view(['GET'])
def list_applications(request):
    data = listapplications(request)
    try:
        data = data.data
        return Response(data=data)
    except:
        return Response({'status':'failed'})


@api_view(['POST'])
def accept_application(request):
    try:
        user = Account.objects.get(username=request.user)
    except:
        return Response({"status": "forbidden"})
    if request.user.is_authenticated and user.is_organization:
        data = request.data
        response = acceptapplication(request,data)
        return Response({'status':response})
    else:
        return Response({'status':'forbidden'})


@api_view(['POST'])
def add_room(request):
    user = request.user
    if user.is_authenticated:
        data = request.data
        response = addroom(request, user, data)
        return Response({"status": response})
    else:
        return Response({'status': 'not allowed'})


@api_view(['GET'])
def list_all_rooms(request):
    user = request.user
    if user.is_authenticated:
        response = listallrooms(request)
        return Response(response.data)
    else:
        return Response({'status': 'not allowed'})


@api_view(['POST'])
def delete_room(request):           # takes room id  as data
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated and user.is_organization:
            data = request.data
            room = Room.objects.filter(organization=user.organization, id=data['room'])
            if len(room) == 0:
                return Response({'status':'no such room'})
            response = deleteroom(room[0])
            return Response({'status': response})
        else:
            raise Exception
    except:
        return Response({"status": "forbidden"})

# Teacher level apis


# Student level apis

