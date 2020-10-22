from django.db import models
from custom_user.models import Room, Account, Teacher


class DashOption(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    link = models.CharField(max_length=512,null=True,blank=True,default="#")
    label = models.CharField(max_length=512)
    method = models.CharField(max_length=512,null=True,blank=True)
    icon = models.CharField(max_length=512,null=True,blank=True,default="insert_emoticon")

    def __str__(self):
        return self.account.first_name


class Course(models.Model):
    c_id = models.CharField(max_length=128, primary_key=True)
    c_name = models.CharField(max_length=255)
    c_description = models.CharField(max_length=512)
    for_organization = models.ForeignKey(Account,on_delete=models.CASCADE)
    for_room = models.ManyToManyField(Room)
    c_status = models.BooleanField(default=False)
    instructor = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.c_name


class Lecture(models.Model):
    for_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    l_number = models.IntegerField()
    l_name = models.CharField(max_length=1024)
    l_url = models.URLField(max_length=1024)
    l_description = models.CharField(max_length=512, null=True,blank=True)

    def __str__(self):
        return self.l_name


class LectureResource(models.Model):
    lr_name = models.CharField(max_length=512)
    lr_description = models.CharField(max_length=1024)
    for_lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE)
    lr_url = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True,upload_to='lecture_resource')


class CourseResource(models.Model):
    cr_name = models.CharField(max_length=512)
    cr_description = models.CharField(max_length=1024)
    for_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    cr_url = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='course_resource')


class Slot(models.Model):
    info = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=500, null=True, blank=True)


class TimeTable(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.ManyToManyField(Slot, null=True, blank=True)
    status = models.CharField(max_length=100, choices=(('enable', 'enable'), ('disable', 'disable')))
