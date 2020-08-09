from rest_framework.decorators import api_view
from rest_framework.response import Response
from management.views import listapplications, addroom, listallrooms, acceptapplication

# organization level apis
@api_view(['GET'])
def list_applications(request):
    data = listapplications(request)
    try:
        data = data.data
        return Response(data=data)
    except:
        return Response({'status':'failed'})


@api_view(['POST'])
def accept_application(request):
    if request.user.is_authenticated and request.user.custom_user.is_organization:
        data = request.data
        response = acceptapplication(request,data)
        return Response({'status':response})
    else:
        return Response({'status':'forbidden'})


@api_view(['POST'])
def add_room(request):
    user = request.user
    if user.is_authenticated:
        data = request.data
        response = addroom(request, user, data)
        return Response({"status": response})
    else:
        return Response({'status': 'not allowed'})


@api_view(['GET'])
def list_all_rooms(request):
    user = request.user
    if user.is_authenticated:
        response = listallrooms(request, user)
        return Response(response.data)
    else:
        return Response({'status': 'not allowed'})


# Teacher level apis


# Student level apis

