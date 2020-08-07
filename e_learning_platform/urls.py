"""e_learning_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from custom_user import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('signup/', user_views.signup),
    path('signin/', user_views.signin),
    path('signout/', user_views.signout),
    path('verify/', user_views.verify_otp),
    path('dashboard/', include('management.urls')),
    path('elibrary/',include('elibrary.urls')),
    path('r/<str:id>', user_views.RegisterStudent),
    path('api/', include('api.urls') ),
    path('testing/',user_views.testing),

]
