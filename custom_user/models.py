from django.db import models
from django.contrib.auth.models import User,AbstractUser


class Custom_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_organization = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Room(models.Model):
    title = models.CharField(max_length=512, default='room', blank=False, null=False)
    description = models.CharField(max_length=1024, default='room description here', blank=False, null=False)
    organization = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)
    display_pic = models.ImageField(blank=True, default=None, null=True)
    room_stream_details = models.CharField(max_length=1024, default='free', blank=False, null=False)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    from_room = models.ForeignKey(Room, blank=True, default=None, null=True, on_delete=models.SET("Doesn't belong to any room"))


class Teacher(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    manages_room = models.ForeignKey(Room, blank=True, default=None, null=True, on_delete=models.SET("Doesn't belong to any room"))


class ApplyForStudent(models.Model):
    first_name = models.CharField(max_length=512,blank=False,null=False)
    last_name = models.CharField(max_length=512)
    email = models.EmailField(max_length=512,blank=False,null=False)
    phone = models.IntegerField()
    for_organization = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    password = models.CharField(max_length=512)
    reference = models.CharField(max_length=100,default=0)
    submissionstamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference