from django.db import models
from django.contrib.auth.models import User


class Organization(User):
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class Room(models.Model):
    pass



