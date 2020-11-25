from django.shortcuts import render, HttpResponse, redirect
from custom_user.models import Room, ApplyForStudent, Student, Account, Teacher, Organization
from management.models import Course, Lecture, CourseResource, DashOption, TimeTable, Assignment, Solution, Slot
from api.serializers import *
from .manager import *
import random
from .forms import AddNewTeacher, AddNewStudent, AddAssignment
from .forms import EditRoom
from rest_framework.decorators import api_view
from api.serializers import AssignmentSerializer
from rest_framework.response import Response
import datetime


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
                                {'link': '#', 'method': 'timetablems()', 'label': 'TimeTable', 'icon': 'view_module'},
                                {'link': '#', 'method': 'listallcourses()', 'label': 'Courses', 'icon': 'school'},
                                {'link': '#', 'method': 'listallteachers()', 'label': 'Teachers', 'icon': 'recent_actors'},
                                {'link': '#', 'method': 'listallstudents()', 'label': 'Students', 'icon': 'groups'},
                                {'link': '#', 'method': 'loadLibraryDashboard()', 'label': 'eLibrary','icon': 'local_library'},
                                #{'link': '#', 'method': '', 'label': 'Email', 'icon': 'mail'},

                                 ]
            options_available = DashOption.objects.filter(account=user)
            extra_options = DashOptionSerializer(options_available,many=True).data
            options_available = default_options+extra_options
            nav_btns = [{'link':'/signout', 'label':'Sign Out'},]

            context = {
                'pagetitle': 'PrimeStudies : Dashboard',
                'u': user_model.first_name.capitalize(),
                'navButtons' : nav_btns,
                'options' : options_available,
                'owner':{'coverpic':"https://atulsingh029.github.io/images/banner2.gif",'title':profile_info.first_name,
                         'lead1':profile_info.bio1, 'lead2': profile_info.bio2
                         , 'link':'/r/'+str(profile_info.id),'label':'Advertisement Page', 'profile_pic':p_url}
            }
            return render(request, template_name='dashboard/odash.html', context=context)
        if user.is_student:
            profile_info = user
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'

            default_options = [{'link': '', 'method': '', 'label': 'Dashboard', 'icon': 'dashboard'},
                              {'link': '#', 'method': 'view_assignments()', 'label': 'Assignments', 'icon': 'work'},
                               {'link': '#', 'method': 'loadLibraryDashboard()', 'label': 'eLibrary', 'icon': 'local_library'},
                               ]
            options_available = DashOption.objects.filter(account=user)
            extra_options = DashOptionSerializer(options_available, many=True).data
            options_available = default_options + extra_options
            nav_btns = [{'link': '/signout', 'label': 'Sign Out'},]
            org = user.student.from_organization.account
            context = {
                'pagetitle': 'PrimeStudies : Dashboard',
                'u': user_model.first_name.capitalize(),
                'navButtons': nav_btns,
                'options': options_available,
                'owner': {'coverpic': "https://atulsingh029.github.io/images/banner2.gif",
                          'title': profile_info.first_name+' '+profile_info.last_name,
                          'lead1': profile_info.bio1, 'room': profile_info.student.from_room.title
                    , 'link': profile_info.url, 'label': 'Advertisement Page', 'profile_pic': p_url,
                          'organization':{'name':org.first_name,'bio1':org.bio2}}
            }
            return render(request, template_name='dashboard/sdash.html', context=context)
        if user.is_teacher:
            profile_info = user
            try:
                p_url = profile_info.profile_pic.url
            except:
                p_url = '#'

            default_options = [{'link': '', 'method': '', 'label': 'Dashboard', 'icon': 'dashboard'},
                               {'link': '/dashboard/assignwork', 'method': '', 'label': 'Assign Work', 'icon': 'work'},
                               {'link': '#', 'method': 'roomstudentsIni()', 'label': 'Students', 'icon': 'groups'},
                               {'link': '#', 'method': 'scheduleclass()', 'label': 'Schedule Online Class',
                                'icon': 'class'},

                               {'link': '#', 'method': 'assignments()', 'label': 'Assignments', 'icon': 'assignment'},
                               {'link': '#', 'method': 'loadLibraryDashboard()', 'label': 'eLibrary', 'icon': 'local_library'},

                               ]
            options_available = DashOption.objects.filter(account=user)
            extra_options = DashOptionSerializer(options_available, many=True).data
            options_available = default_options + extra_options
            nav_btns = [{'link': '/signout', 'label': 'Sign Out'},]

            context = {
                'pagetitle': 'PrimeStudies : Dashboard',
                'u': user_model.first_name.capitalize(),
                'navButtons': nav_btns,
                'options': options_available,
                'owner': {'coverpic': "https://atulsingh029.github.io/images/banner2.gif",
                          'title': profile_info.first_name + ' ' + profile_info.last_name,
                          'lead1': profile_info.bio1
                    , 'link': profile_info.url, 'label': 'Advertisement Page', 'profile_pic': p_url}
            }
            return render(request, template_name='dashboard/tdash.html', context=context)
    else:
        return redirect('/?status=youmustloginfirst')



def add_new_teacher(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization and request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            sex = request.POST['sex']
            try:
                phone = request.POST['phone']
                if phone=='':
                    phone=-1
            except:
                phone = -1
            try:
                profile_pic = request.FILES['profile_pic']
            except:
                profile_pic = ''
            username = student_username_generator(email)
            account = Account(username=username,first_name=first_name,last_name=last_name,sex=sex,email=email,phone=phone,is_teacher=True)
            account.save()
            raw = random.randrange(1000000000,9999999999)
            account.set_password(raw)
            account.bio1 = raw #remove this
            if profile_pic != '':
                account.profile_pic = profile_pic
            account.save()
            teacher = Teacher(user=account,from_organization=user.organization)
            teacher.save()
            send_new_teacher_notification(email=email, name=first_name, institute=user.first_name, pwd=raw)
            return redirect('/dashboard')
        if user.is_organization and request.method == 'GET':
            form = AddNewTeacher()
            context = {
                'form':form,
                'formname':'Add New Teacher',
                'text':'You are adding a new teacher to '+request.user.first_name.title()
            }
            return render(request, context=context, template_name='custom_user/forms.html')


def add_new_student(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization and request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            sex = request.POST['sex']
            room = request.POST['room']
            r = Room.objects.filter(id = room)
            try:
                phone = request.POST['phone']
                if phone == '':
                    phone = -1
            except:
                phone = -1
            try:
                profile_pic = request.FILES['profile_pic']
            except:
                profile_pic = ''
            username = student_username_generator(email)
            account = Account(username=username,first_name=first_name,last_name=last_name,sex=sex,email=email,phone=phone,is_student=True)
            account.save()
            raw = random.randrange(1000000000,9999999999)
            account.set_password(raw)
            account.bio1 = raw #remove this
            if profile_pic != '':
                account.profile_pic = profile_pic
            account.save()
            s = Student(user=account,from_organization=user.organization)
            if len(r)!=0:
                s.from_room = r[0]
            s.save()
            send_direct_admission_notification(email=email,name=first_name,username=username,institute=user.first_name,pwd=raw)
            return redirect('/dashboard')
        if user.is_organization and request.method == 'GET':
            rooms = Room.objects.filter(organization=user.organization,deleted = False)
            e_mid = ''
            for room in rooms:
                e_mid = e_mid+'<option value="'+str(room.id )+'">'+room.title+'</option>'
            form = AddNewStudent()
            e_start ='<tr><th><label for="id_room">Room:</label><br></th><td><select name="room" required id="id_room"><option value="-1" selected>Select Room</option>'
            e_end = '</select></td></tr><br>'
            extra_fields = e_start+e_mid+e_end
            context = {
                'form':form,
                'extra_fields':extra_fields,
                'formname':'Add New Student',
                'text':'You are adding a new student to '+request.user.first_name.title()
            }
            return render(request, context=context, template_name='custom_user/forms.html')


# management api views :
def listapplications(request):
    try:
        user = Account.objects.get(username=request.user)
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
        TimeTable(room=room, status='enable').save()
        return 'success'
    except:
        return 'failed'


def viewroom(room):
    # you are given room object as argument, query all courses under this room and return it
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
    room.deleted = True
    tt = room.timetable
    tt.status = 'disable'
    tt.save()
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


def addnewcourse(title,room_id,description,instructor_id,org):
    c_id = str(random.randrange(10000,99999))+str(random.randrange(10000,99999))
    organization = org
    instructor = Teacher.objects.get(id=instructor_id)
    course = Course(c_id=c_id,c_name=title,c_description=description,for_organization=organization,instructor=instructor)
    course.save()
    if room_id != -1:
        room = Room.objects.get(id=room_id)
        course.for_room.add(room)
        course.save()
        return 'success'
    return {'take_to': 'listallcourses'}


def addexistingcourse(room_id,course_id):
    c = Course.objects.get(c_id=course_id)
    r = Room.objects.get(id = room_id)
    c.for_room.add(r)
    c.save()
    return 'success'


def listallcourses(organization_obj):   # takes organization object and returns all courses under the same
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


def opencourse(c):  # takes course object and returns all the resources and lectures
    lectures = Lecture.objects.filter(for_course=c)
    resources = CourseResource.objects.filter(for_course=c)
    final_list = []
    serial_lectures = LectureSerializer(lectures,many=True)
    serial_resources = CourseResourceSerializer(resources,many=True)
    final_list.append(serial_lectures.data)
    final_list.append(serial_resources.data)
    return final_list


def addresource(user,data):
    c_id = data['c_id']
    course = Course.objects.get(c_id=c_id)
    resource = CourseResource(for_course=course, cr_name=data['title'], cr_description=data['description'],
                     file=data['file'])
    resource.save()
    return 'success'


def addlecture(user,data):
    c_id = data['c_id']
    course = Course.objects.get(c_id = c_id)
    lecture = Lecture(for_course=course, l_number=data['number'] , l_name=data['title'], l_description=data['description'], video=data['video'])
    lecture.save()
    return 'success'


def editlecture(user,data):
    return data


def give_assignment(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            account = Account.objects.filter(username=request.user)
            if account[0].is_teacher:
                data = request.POST
                file = request.FILES
                title = data.get('title')
                description = data.get('description')
                max_marks = data.get('max_marks')
                course = data.get('course')
                problem = file.get('problem')
                if course=='none':
                    return redirect('/dashboard/?status=failed:ASelectACourse')
                c=Course.objects.get(c_id=course)
                assignment = Assignment(name=title,description=description,max_marks=max_marks,for_course=c,problem=problem)
                assignment.save()
                return redirect('/dashboard/?status=added')
        else:
            account = Account.objects.filter(username=request.user)
            if account[0].is_teacher:
                courses = Course.objects.filter(instructor=account[0].teacher)
                form = AddAssignment()
                return render(request, 'custom_user/assignment.html',context={'form':form,'courses':courses, 'formname':'Assign Work'})

def checkAssignment(request):
    pass


#for student only
@api_view(['GET'])
def list_assignments(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_student:
            try:
                room = account[0].student.from_room
                c = Course.objects.filter(for_room=room)
                assignments = []

                for i in c:
                    a = Assignment.objects.filter(for_course=i)
                    #print(a)
                    for j in a:
                        #print(j)
                        s = Solution.objects.filter(solution_to=j, uploader=account[0])
                        #print(s)
                        if len(s) == 0:
                            assignments.append(j)
                serialdata = AssignmentSerializer(assignments, many=True)
                return Response(serialdata.data)
            except:
                return HttpResponse("You are not assigned any room. Please contact your organization first!")


@api_view(['POST'])
def send_sol(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_student:
            file = request.FILES

            sol = Solution(uploader=account[0],solution_to_id=request.POST['id'],solution=request.FILES['solution'])
            sol.save()
            return Response("success")



@api_view(['GET'])
def get_student_by_teacher(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_teacher:
            c = Course.objects.filter(instructor=account[0].teacher)
            student = []
            for i in c:
                room = Room.objects.filter(course=i)
                for j in room:
                    s=Student.objects.filter(from_room=j)
                    student.extend(s)
            student=set(student)
            serialStudent = StudentSerializer(student,many=True)

            return Response(serialStudent.data)


@api_view(['GET'])
def assignments(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        assignments = []
        if account[0].is_teacher:
            c = Course.objects.filter(instructor=account[0].teacher)
            for i in c:
                a = Assignment.objects.filter(for_course=i)
                #assigned_to = Student.objects.filter(from_room=i.from_room)
                assignments.extend(a)
        serialAssignment = AssignmentSerializer(assignments, many=True)
        return Response(serialAssignment.data)


@api_view(['GET'])
def solutions(request, id):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_teacher:
            assignments = Assignment.objects.get(id=id)
            solutions = Solution.objects.filter(solution_to=assignments)
        serialSol = SolutionSerializer(solutions, many=True)
        return Response(serialSol.data)


@api_view(['POST'])
def scheduleclass(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_teacher:
            data1 = request.data
            data = {}
            for i in data1:
                data.update({i['name']:i["value"]})
            agenda = data.get('agenda')
            stime = data.get('stime')
            et1 = int(stime[0:2])+1
            et2 =int(stime[3:5])
            stime = datetime.time(int(stime[0:2]),0)

            etime = datetime.time(et1,0)
            date = data.get('date')
            date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))
            course = data.get('course')
            url = data.get('url')
            c = Course.objects.get(c_id=course)
            room = Room.objects.filter(course=c)
            slots=[]
            if stime>=etime:
                return Response("Start time and end time invalid")
            if date<datetime.date.today():
                return Response("Invalid Date")
            for r in room:
                s = TimeTable.objects.filter(room=r)
                for tt in s:
                    sl = Slot.objects.filter(timetable=tt, start_time=stime, end_time=etime, date=date)
                    for m in sl:
                        slots.append(m)
            if len(slots)!=0:
                return Response("Slot Not Available")
            else:
                ns = Slot(agenda=agenda, start_time=stime, end_time=etime, course=c, session_id=url, date=date)
                ns.save()
                for r in room:
                    s = TimeTable.objects.filter(room=r)
                    for x in s:
                        x.slot.add(ns)
                        x.save()
                return Response("added")


@api_view(['GET'])
def teachers_live_schedule(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_teacher:
            slots = []
            courses = Course.objects.filter(instructor=account[0].teacher)
            for c in courses:
                s= Slot.objects.filter(course=c)
                for i in s:

                    if str(i.date) == str(datetime.datetime.today())[0:10]:

                        slots.append(i)
            print(slots)
            serialslot = SlotSerializer(slots, many=True)
            return Response(serialslot.data)


@api_view(['GET'])
def students_live_schedule(request):
    if request.user.is_authenticated:
        account = Account.objects.filter(username=request.user)
        if account[0].is_student:
            slots = []
            tt = account[0].student.from_room.timetable
            s= Slot.objects.filter(timetable=tt)
            for i in s:

                    if str(i.date) == str(datetime.datetime.today())[0:10]:

                        slots.append(i)

            serialslot = SlotSerializer(slots, many=True)
            return Response(serialslot.data)