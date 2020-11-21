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



def slot_generator(start, end, size):

    '''
    :param start: start is starting time in the format hh:mm am/pm
    :param end: end is ending time in the format hh:mm am/pm
    :param size: size is length of one slot in format hh:mm
    :return: a list of all possible slots
    example :
    start = 10:00 am
    end = 12:00 pm
    size = 01:00
    output format : ['slot name', 'start time', 'end time']
    expected output : [['slot1', 10:00, 11:00],['slot2', 11:00, 12:00]]
    explaination : two slots are possible 10 to 11 and 11 to 12
    '''

    newstarthr = 00
    newstartmin = 00
    newendhr = 00
    newendmin = 00

    # extracting the hour and minute from given time by using string slicing
    if (start.find('am') == -1):

        if (start == '12:00 pm'):
            newstarthr = 12
            newstartmin = 00

        starthr = int(start[0:2]) + 12
        startmin = int(start[3:5])

    else:
        starthr = int(start[0:2])  # for am
        startmin = int(start[3:5])

    if (end.find('am') == -1):

        if (end == '12:00 pm'):
            newendhr = 12
            newendmin = 00

        endhr = int(end[0:2]) + 12
        endmin = int(end[3:5])

    else:
        endhr = int(end[0:2])  # for am
        endmin = int(end[3:5])


    if (newstarthr != 12 and newendhr != 12):

        # converting the hour and minute into total minutes
        totalMin = ((endhr - starthr) * 60) + (endmin - startmin)

        sizehr = int(size[0:2])
        sizemin = int(size[3:5])
        totalsizemin = (sizehr * 60) + sizemin

        hr = int(totalMin / totalsizemin)
        slots = []

        for i in range(1, hr + 1, 1):

            strtime = []
            strtime.append('slot' + str(i))

            starthr = (starthr) % 12
            if (starthr == 0):
                starthr = 12

            strtime.append(str(starthr) + ':' + str(startmin))

            hhr, mmin = divmod(totalsizemin, 60)
            starthr = (starthr + hhr)
            totalmincal = startmin + mmin
            addhr, totalmin = divmod(totalmincal, 60)
            startmin = totalmin
            starthr = (starthr + addhr) % 12

            starthr = (starthr) % 12
            if (starthr == 0):
                starthr = 12

            strtime.append(str(starthr) + ':' + str(startmin))
            slots.append(strtime)


    # when newstarthr is (12:00 pm)
    elif (newstarthr == 12 and newendhr != 12):

        # converting the hour and minute into total minutes
        totalMin = ((endhr - newstarthr) * 60) + (endmin - newstartmin)

        sizehr = int(size[0:2])
        sizemin = int(size[3:5])
        totalsizemin = (sizehr * 60) + sizemin

        hr = int(totalMin / totalsizemin)
        slots = []

        for i in range(1, hr + 1, 1):

            strtime = []
            strtime.append('slot' + str(i))

            newstarthr = (newstarthr) % 12
            if (newstarthr == 0):
                newstarthr = 12

            strtime.append(str(newstarthr) + ':' + str(newstartmin))

            hhr, mmin = divmod(totalsizemin, 60)
            newstarthr = (newstarthr + hhr)
            totalmincal = newstartmin + mmin
            addhr, totalmin = divmod(totalmincal, 60)
            newstartmin = totalmin
            newstarthr = (newstarthr + addhr) % 12

            newstarthr = (newstarthr) % 12
            if (newstarthr == 0):
                newstarthr = 12

            strtime.append(str(newstarthr) + ':' + str(newstartmin))
            slots.append(strtime)


    # when newendhr is (12:00 pm)
    elif (newendhr == 12 and newstarthr != 12):

        # converting the hour and minute into total minutes
        totalMin = ((newendhr - starthr) * 60) + (newendmin - startmin)

        sizehr = int(size[0:2])
        sizemin = int(size[3:5])
        totalsizemin = (sizehr * 60) + sizemin

        hr = int(totalMin / totalsizemin)
        slots = []

        for i in range(1, hr + 1, 1):

            strtime = []
            strtime.append('slot' + str(i))

            starthr = (starthr) % 12
            if (starthr == 0):
                starthr = 12

            strtime.append(str(starthr) + ':' + str(startmin))

            hhr, mmin = divmod(totalsizemin, 60)
            starthr = (starthr + hhr)
            totalmincal = startmin + mmin
            addhr, totalmin = divmod(totalmincal, 60)
            startmin = totalmin
            starthr = (starthr + addhr) % 12

            starthr = (starthr) % 12
            if (starthr == 0):
                starthr = 12

            strtime.append(str(starthr) + ':' + str(startmin))
            slots.append(strtime)

    return slots

