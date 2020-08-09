from django.urls import path
from api.views import add_room,list_all_rooms,list_applications,accept_application


urlpatterns = [
    path('addroom/',add_room),
    path('listallrooms/',list_all_rooms),
    path('listapplications/', list_applications),
    path('acceptapplications/', accept_application),
]