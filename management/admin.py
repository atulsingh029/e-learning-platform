from django.contrib import admin
from .models import *


@admin.register(Course)
class CACourse(admin.ModelAdmin):
    list_display = ('c_id', 'c_name', 'c_description', 'for_organization', 'c_status')


@admin.register(Lecture)
class CALecture(admin.ModelAdmin):
    list_display = ('for_course', 'l_number', 'l_name', 'video')


@admin.register(CourseResource)
class CACourseResource(admin.ModelAdmin):
    list_display = ('cr_name', 'cr_description', 'for_course', 'cr_url')


@admin.register(DashOption)
class CACourseResource(admin.ModelAdmin):
    list_display = ('label','account')


admin.site.register(Slot)


@admin.register(TimeTable)
class CATimeTable(admin.ModelAdmin):
    list_display = ('room',)


@admin.register(Assignment)
class CAAssignment(admin.ModelAdmin):
    list_display = ('name', 'for_course', 'deadline')


@admin.register(Solution)
class CASolution(admin.ModelAdmin):
    list_display = ('uploader', 'solution_to')