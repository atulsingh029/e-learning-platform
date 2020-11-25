from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Room,ApplyForStudent, Student, Teacher, Organization, Advertisement


@admin.register(Account)
class Account(UserAdmin):
    list_display = ['username','id','email','is_staff','first_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('User Type'), {'fields': ('is_organization', 'is_teacher','is_student')}),
        (('Extra Profile Builder'), {'fields': ('bio1', 'bio2', 'sex','url','dob','profile_pic','phone')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )

@admin.register(Organization)
class CARoom(admin.ModelAdmin):
    list_display = ('account',)


@admin.register(Room)
class CARoom(admin.ModelAdmin):
    list_display = ('title', 'id', 'description', 'organization', 'room_stream_details', 'room_status')


@admin.register(ApplyForStudent)
class CAApplyForStudent(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'for_organization', 'password', 'reference', 'submissionstamp', 'for_room', 'status')


@admin.register(Student)
class CAStudent(admin.ModelAdmin):
    list_display = ('user','from_room')


@admin.register(Teacher)
class CATeacher(admin.ModelAdmin):
    list_display = ('user','id')

