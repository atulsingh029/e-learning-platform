from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from .forms import SignUp
import random


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = generate_username(email)
        return HttpResponse('name-'+name+'  email- '+email+'  username generated from generate_username method-'+str(username))
    page_info = {'title':'Sign Up'}
    form = SignUp()
    otp = generate_otp()
    context={
        'signup_form':form,
        'page_info':page_info,
        'otp':otp
    }
    return render(request,template_name='custom_user/forms.html',context=context)


def generate_username(email):
    response = ''
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
