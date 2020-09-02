from django.core.mail import send_mail,send_mass_mail
from custom_user.models import Account


def student_username_generator(email):
    username = email.split('@')[0]
    checker = Account.objects.filter(username=username)
    count = 1
    while len(checker) != 0:
        username = username + str(count)
        checker = Account.objects.filter(username=username)
        count = count + 1
    return username


def send_rejection_mail_to_student(email,name, institute, reference):
    subject = 'Request Rejected'
    message = 'Hey '+name+',\nYour registration request with reference no "'+reference+ '" @'+institute+' is rejected, \n'+'Please contact the organization for more details.'
    #mail([email,],subject,message)


def send_confirmation_mail_to_student(email,name, username, institute, reference):
    subject = 'Request Accepted'
    message = 'Hey '+name+',\nYour registration request with reference no "'+reference+ '" @'+institute+' is accepted, welcome on board.\n'+'Your username for login is "'+username+'" and your password is same as you entered while registration.'
    #mail([email,],subject,message)


def send_direct_admission_notification(email,name,username,institute,pwd):
    subject = 'Welcome Onboard!'
    message = 'Hey ' + name + ',\nWelcome to ' + institute + '.\n' + 'Your username for login is "' + username + '" and your password is '+str(pwd)+'.'
    # mail([email,],subject,message)

def send_new_teacher_notification(email,name,institute,pwd):
    subject = 'Welcome Onboard!'
    message = 'Hey ' + name + ',\nWelcome to ' + institute + '.\n' + 'Your email : ' + email + ' \npassword : '+str(pwd)
    # mail([email,],subject,message)

def mail(emails, subject, message):
    if str(subject) == '':
        subject = 'Message From PrimeStudies'
    send_mail(subject,message,'atul.auth@gmail.com',emails,fail_silently=True)