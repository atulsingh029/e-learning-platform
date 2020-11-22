from django.urls import path
from .views import *


urlpatterns = [
    path('lib/', showcase ),
    path('add/', add_book),
    path('edit/', edit_book),
    path('delete/<int:id>', delete_book)
]