from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='legacy_home'),
    path('v2/', views.home_2, name='homepage'),
]