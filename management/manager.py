from django.core.mail import send_mail,send_mass_mail
from django.contrib.auth.admin import User


def student_username_generator(email):
    username = email.split('@')[0]
    checker = User.objects.filter(username=username)
    count = 1
    while len(checker) != 0:
        username = username + str(count)
        checker = User.objects.filter(username=username)
        count = count + 1
    return username




def send_confirmation_mail_to_student(email,username,institute,reference):
    pass