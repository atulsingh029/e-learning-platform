from django.urls import path
from api.views import *


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
    path('listallteachers/',list_all_teachers)


]