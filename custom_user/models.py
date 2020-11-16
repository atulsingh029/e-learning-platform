from django.db import models
from django.contrib.auth.models import User,AbstractUser


choices = [('male','male'),('female','female'),('organization','organization')]


class Account(AbstractUser):
    bio1 = models.CharField(max_length=1024, null=True, blank=True)
    bio2 = models.CharField(max_length=1024, null=True, blank=True)
    sex = models.CharField(max_length=15, choices=choices, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=1024, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True,upload_to='profile_pictures', default='def_user.png')
    phone = models.IntegerField(null=True,blank=True)
    is_organization = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Organization(models.Model):
    account = models.OneToOneField(Account,on_delete=models.CASCADE)
    def __str__(self):
        return self.account.first_name

class Room(models.Model):
    title = models.CharField(max_length=512, default='room', blank=False, null=False)
    description = models.CharField(max_length=1024, default='room description here', blank=False, null=False)
    organization = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True,blank=True,default=None)
    display_pic = models.ImageField(blank=True, default=None, null=True,upload_to="Room/")
    room_stream_details = models.CharField(max_length=1024, default='free', blank=False, null=False)
    room_status = models.BooleanField(default=False,null=False,blank=False)
    deleted = models.BooleanField(default=False)
    reference = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title




class Student(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    from_room = models.ForeignKey(Room, blank=True, default=None, null=True, on_delete=models.SET_NULL)
    from_organization = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True,blank=True,default=None)


class Teacher(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    from_organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.user.first_name


class ApplyForStudent(models.Model):
    first_name = models.CharField(max_length=512,blank=False,null=False)
    last_name = models.CharField(max_length=512)
    email = models.EmailField(max_length=512,blank=False,null=False)
    phone = models.IntegerField()
    for_organization = models.ForeignKey(Account,on_delete=models.CASCADE)
    password = models.CharField(max_length=512)
    reference = models.CharField(max_length=100,default=0)
    submissionstamp = models.DateTimeField(auto_now=True)
    for_room = models.ForeignKey(Room,on_delete=models.SET_NULL, null=True,default=None,blank=True)
    status = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.reference


class Session(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=50)


class Advertisement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    banner = models.ImageField(upload_to='banner/', null=True, blank=True)
    description = models.CharField(max_length=200, null=True,blank=True)
    adtg = models.CharField(max_length=100, null=True,blank=True)
    active = models.CharField(max_length=200, choices=[('active','active'),], null=True, blank=True)
