from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard ),
    path('addnewteacher/',views.add_new_teacher),
    path('addnewstudent/',views.add_new_student),
    path('assignwork/',views.give_assignment),
    path('listassignments/',views.list_assignments),
    path('send_sol/',views.send_sol),

]