from django.contrib import admin
from .models import Custom_User,Room,ApplyForStudent, Student, Teacher, ExtraProfileInfo


@admin.register(Custom_User)
class CACustomUser(admin.ModelAdmin):
    list_display = ('user', 'is_organization', 'is_teacher', 'is_student')


@admin.register(Room)
class CARoom(admin.ModelAdmin):
    list_display = ('title', 'description', 'organisation', 'room_number', 'display_pic', 'room_stream_details', 'room_status')


@admin.register(ApplyForStudent)
class CAApplyForStudent(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'for_organization', 'password', 'reference', 'submissionstamp', 'for_room', 'status')


@admin.register(Student)
class CAStudent(admin.ModelAdmin):
    list_display = ('user','from_room')


@admin.register(Teacher)
class CATeacher(admin.ModelAdmin):
    list_display = ('user', 'manages_room')

@admin.register(ExtraProfileInfo)
class CAExtraProfileInfo(admin.ModelAdmin):
    list_display = ('user', 'bio1', 'bio2', 'sex', 'url','dob', 'address', 'profile_pic')