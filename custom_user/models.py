from django.db import models
from django.contrib.auth.models import User,AbstractUser


class Custom_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_organization = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Room(models.Model):
    organization = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)




