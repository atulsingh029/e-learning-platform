from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Custom_User
from .forms import SignUp,OTPForm
import random
from django.contrib.auth import login


datatransfer = []

def signup(request):
    global datatransfer
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and len(User.objects.filter(email=email)) == 0:
            password = password1
            otp = generate_otp()
            message = 'Your One Time Password is ' + str(otp)
            datatransfer = [otp, name, email, password]

            send_mail('Verify Your Account', message, 'atul.auth@gmail.com', [email, ], fail_silently=False)
            return redirect('/verify')
        else:
            return redirect('/signup?q=passwdVDFailed')
    page_info = {'title':'Sign Up'}
    form = SignUp()

    context={
        'signup_form':form,
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
    if request.method == 'POST':
        user_otp = request.POST['otp']
        if int(datatransfer[0]) == int(user_otp):
            username = generate_username(datatransfer[2])
            user = User.objects.create_user(username=username, password=datatransfer[3], first_name=datatransfer[1], email=datatransfer[2])
            temp_user = Custom_User.objects.create(user=user, is_organization=True)
            temp_user.save()
            login(request,user)
            return redirect('/dashboard')
        else:
            return redirect('/verify?q=failed')
    otp_form = OTPForm()
    context = {
        'title':'confirm otp',
        'otp_form':otp_form
    }
    return render(request,template_name='custom_user/otp_form.html', context=context)