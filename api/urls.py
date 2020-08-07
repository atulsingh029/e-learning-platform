from django.urls import path
from api.views import add_room,list_all_rooms,list_applications,accept_applications


urlpatterns = [
    path('addroom/',add_room),
    path('listallrooms/',list_all_rooms),
    path('listapplications/', list_applications),
    path('acceptapplications/<str:reference>', accept_applications),
]