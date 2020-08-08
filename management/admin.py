from django.contrib import admin
from .models import Course, Lecture, LectureResource, CourseResource


@admin.register(Course)
class CACourse(admin.ModelAdmin):
    pass


@admin.register(Lecture)
class CALecture(admin.ModelAdmin):
    pass


@admin.register(LectureResource)
class CALectureResource(admin.ModelAdmin):
    pass


@admin.register(CourseResource)
class CACourseResource(admin.ModelAdmin):
    pass

