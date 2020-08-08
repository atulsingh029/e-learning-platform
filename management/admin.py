from django.contrib import admin
from .models import Course,Lecture


@admin.register(Course)
class CACourse(admin.ModelAdmin):
    pass


@admin.register(Lecture)
class CALecture(admin.ModelAdmin):
    pass



