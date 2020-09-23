from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import ApplyForStudent, Account, Organization, Session
from .forms import SignUp,OTPForm,StudentRegister,SignIn
import random
from django.contrib.auth import login,logout
from management.models import Room
from django.contrib.sessions.models import Session as SysSession


DATA_TRANSFER = {}
STUDENT_APPLICATION = {}


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and len(Account.objects.filter(email=email)) == 0:
            password = password1
            otp = generate_otp()
            message = 'Your One Time Password is ' + str(otp)
            data_transfer_key = email[0:4]+str(random.randrange(100000,999999))
            DATA_TRANSFER[data_transfer_key] = [otp, name, email, password]
            send_mail('Verify Your Account', message, 'atul.auth@gmail.com', [email, ], fail_silently=False)
            return redirect('/verify?q=organization&dtk='+data_transfer_key )
        else:
            return redirect('/signup?q=passwdVDFailed')
    page_info = {'title':'Sign Up'}
    form = SignUp()

    context={
        'formname':'Sign Up',
        'form':form,
        'page_info':page_info,

    }
    return render(request,template_name='custom_user/forms.html',context=context)


def generate_username(email):
    # you are given a str email you need return username from that email
    # eg: atul@email.com, so you have to return 'atul' through response variable
    atIndex = email.index('@')
    response = email[0:atIndex]
    checker = Account.objects.filter(username=response)
    count = 1
    while(len(checker) != 0):
        response = response + str(count)
        checker = Account.objects.filter(username=response)
        count = count + 1
    return response


def generate_otp():
    response = random.randrange(100000,999999)
    return response

def verify_otp(request):
    try:
        mode = request.GET['q']
        dtk = request.GET['dtk']
    except:
        return HttpResponse('Error In Parsing URL : Try Again')
    if request.method == 'POST':
        user_otp = request.POST['otp']
        response = Reg(request,mode,user_otp,dtk)
        if response == 200:
            return HttpResponse("success!")
        return redirect(response)
    otp_form = OTPForm()
    context = {
        'title':'confirm otp',
        'form':otp_form,
        'formname': 'Verify OTP',
        'text': 'One time password was sent to your email, please enter to verify your account.'
    }
    return render(request,template_name='custom_user/forms.html', context=context)


def RegisterStudent(request,id,reference):
    user_temp = Account.objects.filter(id=id)
    if len(user_temp) == 0 or user_temp[0].is_organization == False:
        return HttpResponse('bad url')
    if request.method == 'POST':
        try:
            room = Room.objects.get(reference=reference,deleted=False)
        except:
            return HttpResponse("Invalid Room : Room was deleted by owner")
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        for_organization = user_temp[0]
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # fix required : within the same organization don't allow duplicate emails but if a user wants to signup for a different organization with email that already exists in our user model allow him/her.
        if password1 == password2 and len(Account.objects.filter(email=email)) == 0 and len(ApplyForStudent.objects.filter(email=email,for_organization=user_temp[0])) == 0:
            password = password1
            otp = generate_otp()
            message = 'Your One Time Password for registration @'+id+' is ' + str(otp)
            student_transfer_key = email[0:4]+str(random.randrange(1000000,9999999))
            STUDENT_APPLICATION[student_transfer_key] = [otp, first_name, last_name, email, password, phone, for_organization ,room]
            #send_mail('Verify Your Account', message, 'atul.auth@gmail.com', [email, ], fail_silently=True)
            return redirect('/verify?q=student&dtk='+student_transfer_key)
        else:
            return redirect('/r/'+id)

    student_form = StudentRegister()
    context = {'form':student_form,
               'formname': 'Register With '+user_temp[0].first_name,}
    return render(request, template_name='advertisement.html',context=context)


# This function is used for completing the registration once request is received at any respective view function
def Reg(request,mode,otp,dtk):
        if mode == 'organization':
            if int(DATA_TRANSFER[dtk][0]) == int(otp):
                username = generate_username(DATA_TRANSFER[dtk][2])
                user = Account.objects.create_user(username=username, password=DATA_TRANSFER[dtk][3], first_name=DATA_TRANSFER[dtk][1],
                                                email=DATA_TRANSFER[dtk][2], is_organization=True)
                organization = Organization(account=user)
                organization.save()

                DATA_TRANSFER.pop(dtk)
                login(request, user)
                return '/dashboard'
            else:
                return '/verify?q=organization&dtk='+dtk #exception at 2nd pass
        if mode == 'student':
            if int(STUDENT_APPLICATION[dtk][0]) == int(otp):
                student = ApplyForStudent()
                student.first_name = STUDENT_APPLICATION[dtk][1]
                student.last_name = STUDENT_APPLICATION[dtk][2]
                student.email = STUDENT_APPLICATION[dtk][3]
                student.password = STUDENT_APPLICATION[dtk][4]
                student.phone = STUDENT_APPLICATION[dtk][5]
                student.for_organization = STUDENT_APPLICATION[dtk][6]
                student.for_room = STUDENT_APPLICATION[dtk][7]
                student.reference = STUDENT_APPLICATION[dtk][3][0:4] + str(random.randrange(100000, 999999))
                student.save()
                subject = "Application Submission Successful"
                message = "Hey " + STUDENT_APPLICATION[dtk][1] + ", \nYour application for registration @" + STUDENT_APPLICATION[dtk][6].username + ' is successful, you will be informed as soon as it is accepted by the organization.\nYour application reference number is ' + student.reference +'.\nThank You'
                #send_mail(subject,message,'atul.auth@gmail.com',[STUDENT_APPLICATION[dtk][3], ], fail_silently=True)
                STUDENT_APPLICATION.pop(dtk)
                return 200
            else:
                return '/verify?q=student&dtk='+dtk


def signin(request):
    if request.user.is_authenticated:
        return HttpResponse('bad request : not allowed')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = Account.objects.get(email=email)
            except:
                return redirect('/signin?r=nosuchuser')
            response = authenticate(request,username=user.username,password=password)
            if response is not None:
                login(request,response)
                u = Account.objects.get(username=request.user)
                if u.is_student:
                    s = Session.objects.filter(user=u)
                    for i in s:
                        SysSession.objects.get(session_key=i.session_key).delete()
                        Session.objects.get(session_key=i.session_key).delete()
                    session = Session(user=u,session_key=request.session.session_key)
                    session.save()

                return redirect('/dashboard')
            else:
                return redirect('/signin?r=emailorpasswordincorrect')

        form = SignIn()
        context = {'form':form,'formname': 'Sign In',}
        return render(request,template_name='custom_user/forms.html',context=context)


def signout(request):
    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if user.is_student:
            session_key = request.session.session_key
            Session.objects.get(session_key=session_key).delete()
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


def testing(request):
    student = STUDENT_APPLICATION
    organization = DATA_TRANSFER
    return HttpResponse('Student Reg :'+str(student)+'<br> Organization : '+str(organization))
