from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from custom_user.models import Room, Custom_User, ApplyForStudent,ExtraProfileInfo, Student
import random
from api.serializers import ApplicationSerializer, RoomSerializer
from .manager import *


def dashboard(request):
    if request.user.is_authenticated:
        user_model = request.user
        user = Custom_User.objects.get(user=user_model)
        if user.is_organization:
            profile_info = ExtraProfileInfo.objects.get(user = user)
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'
            context = {
                'pagetitle': '',
                'user': user_model.first_name.capitalize(),
                'navButtons' : [{'link':'/signout', 'label':'Sign Out'},{'link':'/settings', 'label':'Settings'}],
                'owner':{'coverpic':"https://atulsingh029.github.io/images/banner2.gif",'title':profile_info.user.user.first_name,
                         'lead1':profile_info.bio1, 'lead2': profile_info.bio2
                         , 'link':profile_info.url,'label':'Advertisement Page', 'profile_pic':p_url}
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


def acceptapplication(request,data):
    reference = data['reference']
    applicant = ApplyForStudent.objects.get(reference=reference)
    if applicant.status:
        return 'duplicate_request'
    application_owner = applicant.for_organization
    if str(request.user.custom_user.user.username) == str(application_owner):
        username = student_username_generator(applicant.email)
        user = User(username=username, first_name=applicant.first_name,
                    last_name=applicant.last_name, password=applicant.password, email=applicant.email,
                    is_active=True, is_staff=False, is_superuser=False)
        user.save()
        c_user = Custom_User(user=user, is_student=True)
        c_user.save()
        ExtraProfileInfo(user=c_user,).save()
        Student(user=c_user,from_room=applicant.for_room).save()
        send_confirmation_mail_to_student(username=username, institute=application_owner.user.first_name, reference=applicant.reference)
        applicant.status = True
        applicant.save()
        return 'success'
    else:
        return 'failed'



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
