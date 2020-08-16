from rest_framework.decorators import api_view
from rest_framework.response import Response
from management.views import *
from custom_user.models import Account, Room, Organization
from management.models import Course, Lecture, CourseResource, LectureResource


# organization level apis
@api_view(['GET'])
def list_students(request):
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated and user.is_organization:
            response = listallstudents(user)
            return Response(response)
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
def reject_application(request):
    try:
        user = Account.objects.get(username=request.user)
    except:
        return Response({"status": "forbidden"})
    if request.user.is_authenticated and user.is_organization:
        data = request.data
        response = rejectapplication(request,data)
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
                return Response({"data":response.data,"title":room.title})
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
            room = Room.objects.filter(organization=user.organization, id=data['id'])
            if len(room) == 0:
                return Response({'status':'no such room'})
            response = deleteroom(room[0])
            return Response({'status': response})
        else:
            raise Exception
    except:
        return Response({"status": "forbidden"})


@api_view(["POST","GET"])
def edit_room(request,room_id):
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user = request.user
                organization = Account.objects.get(username=user).organization
                room = Room.objects.get(id=room_id)
                if organization == room.organization:
                    try:
                        pic = request.FILES['image']
                    except:
                        pic = None
                    if pic is not None:
                        room.display_pic = pic
                    room.title = request.POST['title']
                    room.description = request.POST['description']
                    room.save()
                    return Response({'o_id': organization.account.id,'reference':room.reference })
                else:
                    return Response({'status: not allowed'})
            else:
                return Response({'status: not allowed'})

        except:
            return Response({'status: not allowed'})

    else:
        try:
            if request.user.is_authenticated:
                user = request.user
                organization = Account.objects.get(username=user).organization
                room = Room.objects.get(id=room_id)
                if organization == room.organization:
                    response = RoomSerializer(room)
                    return Response (response.data)
        except:
            return Response({'status: not allowed'})

@api_view(["GET"])
def get_account(request,id):
    user = request.user
    u = Account.objects.get(username=user)
    getacc = Account.objects.get(id=id)
    if user.is_authenticated and u.is_organization and getacc.student.from_room.organization == u.organization:
        response = getaccount(id)
        return Response(response.data)
    else:
        return Response({'status': 'not allowed'})


@api_view(['get'])
def remove_student_from_current_room(request,id):
    user = request.user
    u = Account.objects.get(username=user)
    getacc = Account.objects.get(id=id)
    if user.is_authenticated and u.is_organization and getacc.student.from_room.organization == u.organization:
        response = removestudentfromroom(id)
        return Response({"room_id":response})
    else:
        return Response({'status': 'not allowed'})


@api_view(['POST'])
def change_student_room(request):
    user = request.user
    u = Account.objects.get(username=user)
    s_id = request.POST['student_id']
    getacc = Account.objects.get(id=s_id)
    r_id = request.POST['room_id']
    if user.is_authenticated and u.is_organization and getacc.student.from_room.organization == u.organization:
        response = changestudentroom(student_id=s_id,room_id=r_id)
        return Response({"room_id": response})
    else:
        return Response({'status': 'not allowed'})



@api_view(['POST'])
def add_course(request):
    return HttpResponse("work in progress")

# Teacher level apis


# Student level apis

