from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Custom_User,ApplyForStudent
from .forms import SignUp,OTPForm,StudentRegister,SignIn
import random
from django.contrib.auth import login,logout


DATA_TRANSFER = {}
STUDENT_APPLICATION = {}


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and len(User.objects.filter(email=email)) == 0:
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
    checker = User.objects.filter(username=response)
    count = 1
    while(len(checker) != 0):
        response = response + str(count)
        checker = User.objects.filter(username=response)
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
        'text': 'An one time password was sent to your email, please enter to verify your account.'
    }
    return render(request,template_name='custom_user/forms.html', context=context)


def RegisterStudent(request,id):
    user_temp = User.objects.filter(username=id)
    if len(user_temp) == 0:
        return HttpResponse('bad url')
    user_temp = Custom_User.objects.filter(user=user_temp[0])
    print(user_temp)
    if len(user_temp) == 0 or user_temp[0].is_organization == False:
        return HttpResponse('bad url')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        for_organization = user_temp[0]
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # fix required : within the same organization don't allow duplicate emails but if a user wants to signup for a different organization with email that already exists in our user model allow him/her.
        if password1 == password2 and len(User.objects.filter(email=email)) == 0 and len(ApplyForStudent.objects.filter(email=email)) == 0:
            password = password1
            otp = generate_otp()
            message = 'Your One Time Password for registration @'+id+' is ' + str(otp)
            student_transfer_key = email[0:4]+str(random.randrange(1000000,9999999))
            STUDENT_APPLICATION[student_transfer_key] = [otp, first_name, last_name, email, password, phone, for_organization]
            send_mail('Verify Your Account', message, 'atul.auth@gmail.com', [email, ], fail_silently=False)
            return redirect('/verify?q=student&dtk='+student_transfer_key)
        else:
            return redirect('/r/'+id)

    student_form = StudentRegister()
    context = {'form':student_form,
               'formname': 'Register With '+id,}
    return render(request, template_name='custom_user/forms.html',context=context)


def Reg(request,mode,otp,dtk):
        if mode == 'organization':
            if int(DATA_TRANSFER[dtk][0]) == int(otp):
                username = generate_username(DATA_TRANSFER[dtk][2])
                user = User.objects.create_user(username=username, password=DATA_TRANSFER[dtk][3], first_name=DATA_TRANSFER[dtk][1],
                                                email=DATA_TRANSFER[dtk][2])
                temp_user = Custom_User.objects.create(user=user, is_organization=True)
                temp_user.save()
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
                student.reference = STUDENT_APPLICATION[dtk][3][0:4]+str(random.randrange(100000,999999))
                student.save()
                subject = "Application Submission Successful"
                message = "Hey " + STUDENT_APPLICATION[dtk][1] + ", \nYour application for registration @" + STUDENT_APPLICATION[dtk][6].user.username + ' is successful, you will be informed as soon as it is accepted by the organization.\nYour application reference number is ' + student.reference +'.\nThank You'
                send_mail(subject,message,'atul.auth@gmail.com',[STUDENT_APPLICATION[dtk][3], ], fail_silently=False)
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
            username = User.objects.get(email=email)
            response = authenticate(request,username=username,password=password)
            if response is not None:
                login(request,response)
                return redirect('/dashboard')
            else:
                return redirect('/signin')

        form = SignIn()
        context = {'form':form,'formname': 'Sign In',}
        return render(request,template_name='custom_user/forms.html',context=context)

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')
