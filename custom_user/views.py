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
    # author: abhishek
    # you are given a str email you need return username from that email
    # eg: atul@email.com, so you have to return 'atul' through response variable
    ''' use function User.objects.filter(username = 'atul') i.e. username is the one you just extracted, if this method 
     returns empty queryset then return same username eg. 'atul' but if you get non empty queryset then append a number
     at end of username eg. 'atul_1' because username is primary key in database and it should not be duplicated '''
    return response


def generate_otp():
    response = random.randrange(100000,999999)
    return response
