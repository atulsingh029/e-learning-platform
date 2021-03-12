from django.urls import path
from api.views import *

#TODO : standardize all end points
urlpatterns = [
    path('addroom/',add_room),
    path('listallrooms/',list_all_rooms),
    path('listapplications/', list_applications),
    path('acceptapplications/', accept_application),
    path('rejectapplications/', reject_application),
    path('deleteroom/',delete_room),
    path('listallstudents/', list_students),
    path('listroomstudents/<int:room_id>/', list_room_students),
    path('viewroom/<int:room_id>', view_room),
    path('editroom/<int:room_id>', edit_room),
    path('getaccount/<int:id>', get_account),
    path('removestudentfromcurrentroom/<int:id>', remove_student_from_current_room),
    path('changestudentroom/',change_student_room),
    path('listallcourses/',list_all_courses),
    path('addcourse/<str:type>/',add_course),
    path('listallteachers/',list_all_teachers),
    path('opencourse/<str:c_id>/',open_course),
    path('viewstudentroom/',view_student_room),
    path('search/',search),
    path('getbook/<str:id>/', get_book),
    path('deletecourseresource/<str:id>/', delete_resource ),
    path('deletelecture/<str:id>/', delete_lecture ),
    path('addcourseresource/', add_resource),
    path('addlecture/', add_lecture),
    path('editlecture/', edit_lecture),
    path('getteacherscourse', get_teachers_course),
]

# Version 2.0.0 Endpoints
urlpatterns = urlpatterns + [
    path('user/get/<str:operation>/', get_user),
    path('user/post/<str:operation>/', post_user),
    path('room/get/<str:operation>/', get_room),
    path('room/post/<str:operation>/', post_room),
    path('course/get/<str:operation>/', get_course),
    path('course/post/<str:operation>/', post_course),
    path('lecture/get/<str:operation>/', get_lecture),
    path('lecture/post/<str:operation>/', post_lecture),
    path('library/get/<str:operation>/', get_library),
    path('library/post/<str:operation>/', post_library),
    path('application/get/<str:operation>/', get_application),
    path('application/post/<str:operation>/', post_application),
]