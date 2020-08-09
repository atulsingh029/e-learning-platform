from django.contrib import admin
from .models import Course, Lecture, LectureResource, CourseResource


@admin.register(Course)
class CACourse(admin.ModelAdmin):
    list_display = {'c_id', 'c_name', 'c_description', 'for_organization', 'for_room', 'c_status'}


@admin.register(Lecture)
class CALecture(admin.ModelAdmin):
    list_display = ('for_course', 'l_number', 'l_name', 'l_url')


@admin.register(LectureResource)
class CALectureResource(admin.ModelAdmin):
    list_display = ('lr_name', 'lr_description', 'for_lecture', 'lr_url', 'file')


@admin.register(CourseResource)
class CACourseResource(admin.ModelAdmin):
    list_display = ('cr_name', 'cr_description', 'for_course', 'cr_url', 'file')
