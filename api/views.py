from rest_framework.decorators import api_view
from rest_framework.response import Response
from management.views import *
from custom_user.models import Account, Room, Organization
from management.models import Course, Lecture, CourseResource, LectureResource
from management.forms import EditRoom


# organization level apis
@api_view(['GET'])
def list_students(request):
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated and user.is_organization:
            response = listallstudents(user)
            return Response(response.data)
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
                    return Response(response.data)
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


# this api call returns all the courses inside specified room id for authenticated user
@api_view(['GET'])
def view_room(request,room_id):
    try:
        if request.user.is_authenticated:
            user = request.user
            organization = Account.objects.get(username=user).organization
            room = Room.objects.get(id=room_id)
            if organization == room.organization:
                response = viewroom(room)
                return Response(response.data)
            else:
                return Response({'status': 'not allowed'})
        else:
            return Response({'status': 'not allowed'})
    except:
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


@api_view(['GET'])
def edit_room(request,room_id):
    try:
        if request.user.is_authenticated:
            user = request.user
            organization = Account.objects.get(username=user).organization
            room = Room.objects.get(id=room_id)

            if organization == room.organization:
                form = EditRoom(initial={'title':room.title,'description':room.description})
                return HttpResponse(str(form.as_ul()),content_type='text/plain')
            else:
                return Response({'status': 'not allowed'})
        else:
            return Response({'status': 'not allowed'})
    except:
        return Response({'status': 'not allowed'})



# Teacher level apis


# Student level apis

