from django.shortcuts import render, HttpResponse, redirect
from custom_user.models import Room, ApplyForStudent, Student, Account
import random
from api.serializers import ApplicationSerializer, RoomSerializer
from .manager import *


def dashboard(request):
    if request.user.is_authenticated:
        user_model = request.user
        user = Account.objects.get(username=user_model)
        if user.is_organization:
            profile_info = user
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'
            context = {
                'pagetitle': '',
                'user': user_model.first_name.capitalize(),
                'navButtons' : [{'link':'/signout', 'label':'Sign Out'},{'link':'/settings', 'label':'Settings'}],
                'owner':{'coverpic':"https://atulsingh029.github.io/images/banner2.gif",'title':profile_info.first_name,
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
    try:
        user = Account.objects.get(username = request.user)
    except:
        return {"status": "forbidden"}
    if request.user.is_authenticated and user.is_organization:
        data = ApplyForStudent.objects.filter(for_organization=user)
        serial_data = ApplicationSerializer(data.all(), many=True)
        return serial_data
    else:
        return {"status": "forbidden"}


def acceptapplication(request,data):
    try:
        user = Account.objects.get(username=request.user)
    except:
        return {"status": "forbidden"}
    reference = data['reference']
    applicant = ApplyForStudent.objects.get(reference=reference)
    if applicant.status:
        return 'duplicate_request'
    application_owner = applicant.for_organization
    if user == application_owner:
        username = student_username_generator(applicant.email)
        user = Account(username=username, first_name=applicant.first_name,
                    last_name=applicant.last_name, password=applicant.password, email=applicant.email,
                    is_active=True, is_staff=False, is_superuser=False, is_student=True)
        user.save()
        Student(user=user,from_room=applicant.for_room).save()
        send_confirmation_mail_to_student(email=applicant.email,name = applicant.first_name,username=username, institute=application_owner.first_name, reference=applicant.reference)
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
        temp = Account.objects.filter(username=user)
        room.organization = temp[0].organization
        room.save()
        return 'success'
    except:
        return 'failed'


def listallrooms(request):
    try:
        user_temp = Account.objects.get(username=request.user)
    except:
        return {"status": "forbidden test"}
    data = Room.objects.filter(organization=user_temp.organization, deleted=False)
    serial_data = RoomSerializer(data.all(), many=True)
    return serial_data


def deleteroom(room):
    # you are given room object as argument, this room object has property deleted, you have to set that attribute to true and it to database
    return 'pass'


def listallstudents(current_loggin_account):
    # you have currently logged in organization as argument(Account object), query the database and return the list of all students under this organization
    return 'pass'


def listroomstudents(room_id):
    # you have room_id as argument(Room object attribute), query the database and return the list of all students in this room
    return 'pass'