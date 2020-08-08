from django.db import models
from custom_user.models import Custom_User,Room


class Course(models.Model):
    c_id = models.CharField(max_length=128, primary_key=True)
    c_name = models.CharField(max_length=255)
    c_description = models.CharField(max_length=512)
    for_organization = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    for_room = models.ManyToManyField(Room)
    c_status = models.BooleanField(default=False)


    def __str__(self):
        return self.c_name


class Lecture(models.Model):
    for_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    l_number = models.IntegerField()
    l_name = models.CharField(max_length=1024)
    l_url = models.URLField(max_length=1024)

    def __str__(self):
        return self.l_name


