from rest_framework.decorators import api_view
from rest_framework.response import Response
from elibrary.models import Library
from management.views import *
from custom_user.models import Account, Room, Organization
from management.models import Course, Lecture, CourseResource



# organization level apis
@api_view(['POST'])
def search(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            key = request.data['key']
            str(key).lower()
            if (str(key).startswith('+91')):
                temp_p_key = str(key).replace('+91', '')
            else:
                temp_p_key = key
            email_flag = str(key).find('@')
            phone_flag = str(temp_p_key).isdigit()
            phone_flag2 = len(str(temp_p_key))

            if user.is_teacher:
                if str(key).startswith('@'):
                    temp_key = str(key).replace('@', '')
                    teachers = Teacher.objects.filter(user__username=temp_key, from_organization=user.teacher.from_organization)
                    students = Student.objects.filter(user__username=temp_key, from_organization=user.teacher.from_organization)
                    teachers = TeacherSerializer(teachers, many=True)
                    students = StudentSerializer(students, many=True)
                    return Response({"teacher": teachers.data, "student": students.data})

                elif email_flag != -1:
                    teachers = Teacher.objects.filter(user__email=key, from_organization=user.teacher.from_organization)
                    students = Student.objects.filter(user__email=key, from_organization=user.teacher.from_organization)
                    teachers = TeacherSerializer(teachers, many=True)
                    students = StudentSerializer(students, many=True)
                    return Response({"teacher": teachers.data, "student": students.data})

                elif phone_flag and phone_flag2 == 10:
                    teachers = Teacher.objects.filter(user__phone=temp_p_key, from_organization=user.teacher.from_organization)
                    students = Student.objects.filter(user__phone=temp_p_key, from_organization=user.teacher.from_organization)
                    teachers = TeacherSerializer(teachers, many=True)
                    students = StudentSerializer(students, many=True)
                    return Response({"teacher": teachers.data, "student": students.data})

                else:
                    temp = str(key).split(' ')
                    first_name = temp[0]
                    try:
                        last_name = temp[1]
                    except(IndexError):
                        last_name = ''
                    teachers = Teacher.objects.filter(from_organization=user.teacher.from_organization,
                                                      user__first_name__contains=first_name,
                                                      user__last_name__contains=last_name)
                    students = Student.objects.filter(user__first_name__contains=first_name,
                                                      user__last_name__contains=last_name,
                                                      from_organization=user.teacher.from_organization)
                    teachers = TeacherSerializer(teachers, many=True)
                    students = StudentSerializer(students, many=True)

                    return Response({"teacher": teachers.data, "student": students.data})

            if str(key).startswith('@'):
                temp_key = str(key).replace('@','')
                teachers = Teacher.objects.filter(user__username=temp_key, from_organization=user.organization)
                students = Student.objects.filter(user__username=temp_key, from_organization=user.organization)
                teachers = TeacherSerializer(teachers, many=True)
                students = StudentSerializer(students, many=True)
                return Response({"teacher": teachers.data, "student": students.data})

            elif email_flag != -1:
                teachers = Teacher.objects.filter(user__email=key,from_organization=user.organization)
                students = Student.objects.filter(user__email=key,from_organization=user.organization)
                teachers = TeacherSerializer(teachers,many=True)
                students = StudentSerializer(students,many=True)
                return Response({"teacher":teachers.data,"student":students.data})

            elif phone_flag and phone_flag2 == 10:
                teachers = Teacher.objects.filter(user__phone=temp_p_key, from_organization=user.organization)
                students = Student.objects.filter(user__phone=temp_p_key, from_organization=user.organization)
                teachers = TeacherSerializer(teachers, many=True)
                students = StudentSerializer(students, many=True)
                return Response({"teacher": teachers.data, "student": students.data})

            else:
                temp = str(key).split(' ')
                first_name = temp[0]
                try:
                    last_name = temp[1]
                except(IndexError):
                    last_name =''
                teachers = Teacher.objects.filter( from_organization=user.organization, user__first_name__contains=first_name, user__last_name__contains=last_name)
                students = Student.objects.filter(user__first_name__contains=first_name, user__last_name__contains=last_name, from_organization=user.organization)
                teachers = TeacherSerializer(teachers, many=True)
                students = StudentSerializer(students, many=True)

                return Response({"teacher": teachers.data, "student": students.data})


    else:
        return Response({"status":"forbidden"})


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
    s_id = request.data['student_id']
    getacc = Account.objects.get(id=s_id)
    r_id = request.data['room_id']
    if user.is_authenticated and u.is_organization and getacc.student.from_organization == u.organization:
        response = changestudentroom(student_id=s_id, room_id=r_id)
        return Response({"room_id": response})
    else:
        return Response({'status': 'not allowed'})



@api_view(['POST'])
def add_course(request,type):
    if request.user.is_authenticated:
        user = request.user
        u = Account.objects.get(username=user)
        if type == 'new':
            title = request.data['title']
            description = request.data['description']
            room_id = request.data['room_id']
            if room_id == -1:
                o = Organization(id=-1)
                r = Room(reference=-1, organization=o)
            else:
                r = Room.objects.get(id=room_id)
            teacher_account_id = request.data['teacher_id']
            t_a = Account.objects.get(id=teacher_account_id)
            teacher = Teacher.objects.get(user=t_a)
            response = addnewcourse(title, room_id, description, teacher.id,u)
            if response != 'success':
                return Response(response)
            return Response({"o_id": r.organization.id, "reference": r.reference})
        elif type == 'existing':
            r_id = request.data['room_id']
            r = Room.objects.get(id=r_id)
            if request.user.is_authenticated and u.organization.account == r.organization.account:
                addexistingcourse(r_id, request.data['c_id'])
                return Response({"o_id": r.organization.id, "reference": r.reference})


# api to return list of all the active courses running under particular organization
@api_view(['GET'])
def list_all_courses(request):
    user = request.user
    u = Account.objects.get(username=user)
    if request.user.is_authenticated and u.is_organization:
        org_obj = Organization.objects.filter(account=u)
        data = listallcourses(org_obj[0])
        return Response(data.data)


@api_view(['GET'])
def list_all_teachers(request):
    try:
        user = Account.objects.get(username=request.user)
        if request.user.is_authenticated and user.is_organization:
            response = listallteachers(user)
            return Response(response)
        else:
            raise Exception
    except:
        return Response({"status": "forbidden"})


@api_view(['POST'])
def add_lecture(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            data = request.data
            response = addlecture(user,data)
            return Response({"status" : response})
        else:
            return Response({"status": "forbidden"})
    else:
        return Response({"status": "you are not authenticated"})


@api_view(['POST'])
def add_resource(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            data = request.data
            response = addresource(user, data)
            return Response({"status": response})
        else:
            return Response({"status": "forbidden"})
    else:
        return Response({"status": "you are not authenticated"})


@api_view(['POST'])
def edit_lecture(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            data = request.data
            response = editlecture(user, data)
            return Response({"status":response})
        else:
            return Response({"status": "forbidden"})
    else:
        return Response({"status": "you are not authenticated"})


@api_view(['GET'])
def delete_lecture(request,id):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            l_f = Lecture.objects.filter(id=id)
            if len(l_f) != 0:
                l = l_f[0]
                if l.for_course.for_organization == user.organization.account:
                    l.delete()
                    return Response({"status": "success"})
                else:
                    return Response({"status": "forbidden"})
            else:
                return Response({"status": "no such id"})
        else:
            return Response({"status": "forbidden"})
    else:
        return Response({"status": "you are not authenticated"})


@api_view(['GET'])
def delete_resource(request,id):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_organization or user.is_teacher:
            r_f = CourseResource.objects.filter(id=id)
            if len(r_f) != 0:
                r = r_f[0]
                if r.for_course.for_organization == user.organization.account:
                    r.delete()
                    return Response({"status": "success"})
                else:
                    return Response({"status": "forbidden"})
            else:
                return Response({"status": "no such id"})
        else:
            return Response({"status": "forbidden"})
    else:
        return Response({"status": "you are not authenticated"})


@api_view(['GET'])
def open_course(request, c_id):
    if request.user.is_authenticated:
        user = request.user
        u = Account.objects.get(username=user)
        c = Course.objects.get(c_id=c_id)
        rooms = c.for_room.all()
        test = False
        try :
            if u.organization.account == c.for_organization:
                test = True
        except:
            pass
        try :
            if u.teacher == c.instructor:
                test = True
        except:
            pass
        try :
            if u.student.from_room in rooms:
                test = True
        except:
            pass

        if test:
            response = opencourse(c)
            if len(response[0])==0 and len(response[1])==0:
                return Response({"response":"no data available"})
            return Response(response)
        else:
            return Response({"response": "no data available"})


# Student api
@api_view(['GET'])
def view_student_room(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            student = Account.objects.get(username=user).student
            room = student.from_room
            response = viewroom(student.from_room)
            return Response({"data":response.data,"title":room.title})
        else:
            return Response({'status': 'not allowed'})
    except:
        return Response({'status': 'not allowed'})


# library api

@api_view(['GET'])
def get_book(request, id):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        book = Book.objects.get(id=id)
        library = book.library
        if user.organization.account == library.owner.account:
            s_b = BookSerializer(book)
            data = book.bookreview.textreviews_set
            reviews = TextReviewSerializer(data, many=True)
            return Response({'book': s_b.data, 'comments': reviews.data})
        else:
            return Response({'status': 'forbidden'})
    else:
        return Response({'status':'forbidden'})


@api_view(['GET'])
def get_teachers_course(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_teacher:
            c = Course.objects.filter(instructor=user.teacher)
            serialdata = CourseSerializer1(c,many=True)
            return Response(serialdata.data)