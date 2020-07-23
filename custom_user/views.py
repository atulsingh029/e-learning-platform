from django.shortcuts import render
from django.contrib.auth.models import User


def generateUsername(email):
    response = ''
    # author: abhishek
    # you are given a str email you need return username from that email
    # eg: atul@email.com, so you have to return 'atul' through response variable
    ''' use function User.objects.filter(username = 'atul') i.e. username is the one you just extracted, if this method 
     returns empty queryset then return same username eg. 'atul' but if you get non empty queryset then append a number
     at end of username eg. 'atul_1' because username is primary key in database and it should not be duplicated '''
    return response
