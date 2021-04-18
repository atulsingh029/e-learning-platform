from django.db import models
from custom_user.models import Room, Account, Teacher, Student


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
    video = models.FileField(upload_to='videos')
    l_description = models.CharField(max_length=512, null=True,blank=True)

    def __str__(self):
        return self.l_name


class CourseResource(models.Model):
    cr_name = models.CharField(max_length=512)
    cr_description = models.CharField(max_length=1024)
    for_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    cr_url = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='course_resource')


class Assignment(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    for_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    max_marks = models.IntegerField(null=True, blank=True)
    problem = models.FileField(blank=True, null=True, upload_to='assignment/problem')


class Solution(models.Model):
    uploader = models.ForeignKey(Account, on_delete=models.CASCADE)
    solution_to = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    solution = models.FileField(upload_to='assignment/solution')
    marks = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=512, null=True, blank=True)


class LiveSessionRequest(models.Model):
    requester = models.ForeignKey(Student, on_delete=models.CASCADE)
    for_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    for_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.CharField(null=True, blank=True, max_length=2048)
    status = models.CharField(max_length=50, choices=(('accepted', 'accepted'),('requested', 'requested'),('rejected', 'rejected')), default='requested')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    webrtc_offer = models.CharField(max_length=500000, null=True, blank=True)
    webrtc_answer = models.CharField(max_length=500000, null=True, blank=True)


class Slot(models.Model):
    agenda = models.CharField(max_length=512, default="default", null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, choices=(('rtc', 'rtc'), ('3rd party', '3rd party')))
    session_id = models.CharField(max_length=500, null=True, blank=True)
    web_rtc_request = models.ForeignKey(LiveSessionRequest, on_delete=models.CASCADE, null=True, blank=True)


class TimeTable(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.ManyToManyField(Slot)
    status = models.CharField(max_length=100, choices=(('enable', 'enable'), ('disable', 'disable')))




