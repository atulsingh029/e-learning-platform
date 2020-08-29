from django.shortcuts import render, HttpResponse, redirect
from custom_user.models import Room, ApplyForStudent, Student, Account, Teacher, Organization
from management.models import Course, Lecture, CourseResource, LectureResource, DashOption
from api.serializers import ApplicationSerializer, RoomSerializer, DashOptionSerializer, CourseSerializer, StudentSerializer, AccountSerializer, CustomStudentSerializer
from .manager import *
import random
from .forms import EditRoom


def dashboard(request):
    try:
        message = request.GET['q']
    except:
        message =""
    if request.user.is_authenticated:
        user_model = request.user
        user = Account.objects.get(username=user_model)
        if user.is_organization:
            profile_info = user
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'

            default_options = [{'link':'','method':'','label':'Dashboard', 'icon':'dashboard'},
                               {'link': '#', 'method': 'listapplications()', 'label': 'Applications',
                                'icon': 'group_add'},
                                {'link':'#','method':'listallrooms()','label':'Rooms', 'icon':'class'},
                                {'link': '#', 'method': 'listallcourses()', 'label': 'Courses', 'icon': 'school'},
                                {'link': '#', 'method': 'listallteachers()', 'label': 'Teachers', 'icon': 'recent_actors'},
                                {'link': '#', 'method': 'listallstudents()', 'label': 'Students', 'icon': 'groups'},
                                {'link': '#', 'method': '', 'label': 'eLibrary','icon': 'local_library'},

                                 ]
            options_available = DashOption.objects.filter(account=user)
            extra_options = DashOptionSerializer(options_available,many=True).data
            options_available = default_options+extra_options
            nav_btns = [{'link':'/signout', 'label':'Sign Out'},{'link':'/settings', 'label':'Settings'}]

            context = {
                'pagetitle': 'PrimeStudies : Dashboard',
                'user': user_model.first_name.capitalize(),
                'navButtons' : nav_btns,
                'options' : options_available,
                'owner':{'coverpic':"https://atulsingh029.github.io/images/banner2.gif",'title':profile_info.first_name,
                         'lead1':profile_info.bio1, 'lead2': profile_info.bio2
                         , 'link':profile_info.url,'label':'Advertisement Page', 'profile_pic':p_url}
            }
            return render(request, template_name='dashboard/odash.html', context=context)
        if user.is_student:
            profile_info = user
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'

            default_options = [{'link': '', 'method': '', 'label': 'Dashboard', 'icon': 'dashboard'},
                               {'link': '#', 'method': '', 'label': 'Teachers', 'icon': 'recent_actors'},
                               {'link': '#', 'method': '', 'label': 'eLibrary', 'icon': 'local_library'},
                               ]
            options_available = DashOption.objects.filter(account=user)
            extra_options = DashOptionSerializer(options_available, many=True).data
            options_available = default_options + extra_options
            nav_btns = [{'link': '/signout', 'label': 'Sign Out'}, {'link': '/settings', 'label': 'Settings'}]

            context = {
                'pagetitle': 'PrimeStudies : Dashboard',
                'user': user_model.first_name.capitalize(),
                'navButtons': nav_btns,
                'options': options_available,
                'owner': {'coverpic': "https://atulsingh029.github.io/images/banner2.gif",
                          'title': profile_info.first_name,
                          'lead1': profile_info.bio1, 'lead2': profile_info.bio2
                    , 'link': profile_info.url, 'label': 'Advertisement Page', 'profile_pic': p_url}
            }
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
        data = ApplyForStudent.objects.filter(for_organization=user,status=False, rejected=False)
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
                    last_name=applicant.last_name, email=applicant.email,
                    is_active=True, is_staff=False, is_superuser=False, is_student=True)
        user.set_password(applicant.password)
        user.save()
        Student(user=user,from_room=applicant.for_room,from_organization=applicant.for_organization.organization).save()
        send_confirmation_mail_to_student(email=applicant.email,name = applicant.first_name,username=username, institute=application_owner.first_name, reference=applicant.reference)
        applicant.status = True
        applicant.save()
        return 'success'
    else:
        return 'failed'


def rejectapplication(request,data):
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
        send_rejection_mail_to_student(email=applicant.email,name = applicant.first_name, institute=application_owner.first_name, reference=applicant.reference)
        applicant.rejected = True
        applicant.save()
        return 'success'
    else:
        return 'failed'


def addroom(request, user, data):
    try:
        room = Room()
        room.title = data['title']
        room.description = data['description']
        room.display_pic = request.FILES.get('display_pic')
        temp = Account.objects.filter(username=user)
        room.organization = temp[0].organization
        room.reference = temp[0].organization.account.username+str(random.randrange(111111,999999))
        room.save()
        return 'success'
    except:
        return 'failed'


def viewroom(room):
    # you are given room object as argument, query all courses under this room and return it
    '''try:
        user_temp = Account.objects.get(username=room.user)
    except:
        return {"status": "forbidden test"}
    data = Room.objects.filter(course=user_temp.course, deleted=False)
    serial_data = RoomSerializer(data.all(), many=True)

    return serial_data'''

    data = Course.objects.filter(for_room=room)
    serial_data = CourseSerializer(data.all(), many=True)
    return serial_data


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
    '''try:
        user_temp = Account.objects.get(username=room.user)
    except:
        return {"status": "forbidden test"}
    data = Room.objects.filter(room=user_temp.room, deleted=True)
    serial_data = RoomSerializer(data.all(), many=True)'''
    room.deleted = True
    room.save()
    data = Student.objects.filter(from_room=room)
    for i in data:
        i.from_room = None
        i.save()
    return 'success'

def removestudentfromroom(student_id):
    user = Account.objects.get(id=student_id)
    r_id = user.student.from_room.id
    s = user.student
    s.from_room = None
    s.save()
    return r_id

def changestudentroom(student_id,room_id):
    user = Account.objects.get(id=student_id)
    room = Room.objects.get(id=room_id)
    s = user.student
    s.from_room = room
    s.save()
    return "success"


def listallstudents(current_loggin_account):
    # you have currently logged in organization as argument(Account object), query the database and return the list of all students under this organization
    students = Student.objects.filter(from_organization=current_loggin_account.organization)
    final_list = []
    for student in students:
        user = student.user
        serial_user = AccountSerializer(user,many=False)
        temp = dict(serial_user.data)
        temp.update({"room":student.from_room})
        final_list.append(temp)
    data = CustomStudentSerializer(final_list,many=True)
    return data.data


def listroomstudents(room_id):
    # you have room_id as argument(Room object attribute), query the database and return the list of all students in this room
    try:
        room = Room.objects.get(id=room_id)
        data = Student.objects.filter(from_room=room)
        final_list=[]
        for i in data:
            temp = Account.objects.get(id=i.user.id)
            final_list.append(temp)
        data = AccountSerializer(final_list,many=True)
        return data
    except:
        return {"status": "forbidden"}


def getaccount(account_id):
    data = Account.objects.get(id=account_id)
    data = AccountSerializer(data)
    return data


def addnewcourse(title,room_id,organization_id,description,instructor_id):
    c_id = str(random.randrange(10000,99999))+str(random.randrange(10000,99999))
    room = Room.objects.get(ud=room_id)
    organization = Organization.objects.get(id = organization_id)
    instructor = Teacher.objects.get(id=instructor_id)
    course = Course(c_id=c_id,c_name=title,c_description=description,for_organization=organization,instructor=instructor,for_room=room)
    course.save()
    return 'success'

def addexistingcourse(room_id,course_id):
    c = Course.objects.get(c_id=course_id)
    r = Room.objects.get(id = room_id)
    c.for_room.add(r)
    c.save()
    return 'success'


def listallcourses(organization_obj):   #takes organization object as argument and returns serialized list of all courses under the same
    c = Course.objects.filter(for_organization=organization_obj.account,)
    serial_data = CourseSerializer(c,many=True)
    return serial_data


def listallteachers(user):
    teachers = Teacher.objects.filter(from_organization=user.organization)
    final_list = []
    for teacher in teachers:
        user = teacher.user
        serial_user = AccountSerializer(user, many=False)
        temp = dict(serial_user.data)
        final_list.append(temp)
    return final_list