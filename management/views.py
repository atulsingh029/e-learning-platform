from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from custom_user.models import Room, Custom_User, ApplyForStudent
import random
from api.serializers import ApplicationSerializer, RoomSerializer


def dashboard(request):
    if request.user.is_authenticated:
        user_model = request.user
        user = Custom_User.objects.get(user=user_model)
        if user.is_organization:
            context = {
                'pagetitle': '',
                'user': user_model.first_name.capitalize(),
            }
            return render(request, template_name='dashboard/odash.html', context=context)
        if user.is_student:
            context = {}
            return render(request, template_name='dashboard/sdash.html', context=context)
        if user.is_teacher:
            context = {}
            return render(request, template_name='dashboard/tdash.html', context=context)
    else:
        return redirect('/signin')


# management api views :
def listapplications(request):
    if request.user.is_authenticated and request.user.custom_user.is_organization:
        user = request.user
        data = ApplyForStudent.objects.filter(for_organization__user=user)
        serial_data = ApplicationSerializer(data.all(), many=True)
        return serial_data
    else:
        return {"status": "forbidden"}


def addroom(request, user, data):
    try:
        room = Room()
        room.title = data['title']
        room.description = data['description']
        temp = User.objects.filter(username=str(user))
        temp = Custom_User.objects.filter(user=temp[0])
        room.organization = temp[0]
        room.room_number = random.randrange(0, 9999999)  # only for testing : reimplementation required
        room.save()
        return 'success'
    except:
        return 'failed'


def listallrooms(request, user):
    temp = Custom_User.objects.get(user_id=user.id)
    data = Room.objects.filter(organization_id=temp.id)
    serial_data = RoomSerializer(data.all(), many=True)
    return serial_data
