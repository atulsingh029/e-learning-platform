from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard ),
    path('addnewteacher/',views.add_new_teacher),
    path('addnewstudent/',views.add_new_student)

]