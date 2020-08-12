from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard ),
    path('editroom/<str:id>/',views.edit_room),


]