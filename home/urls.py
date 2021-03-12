from django.urls import path
from . import views

urlpatterns = [
    path('v1/', views.home, name='legacy_home'),
    path('', views.home_2, name='homepage'),
]