from django.contrib import admin
from .models import Custom_User,Room,ApplyForStudent, Student, Teacher


@admin.register(Custom_User)
class CACustomUser(admin.ModelAdmin):
    list_display = ('user', 'is_organization', 'is_teacher', 'is_student')


@admin.register(Room)
class CARoom(admin.ModelAdmin):
    pass


@admin.register(ApplyForStudent)
class CAApplyForStudent(admin.ModelAdmin):
    pass


@admin.register(Student)
class CAStudent(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class CATeacher(admin.ModelAdmin):
    pass