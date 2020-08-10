from rest_framework import serializers
from custom_user.models import ApplyForStudent, Room, Account


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForStudent
        fields = ['id','first_name','last_name','email','phone','reference','submissionstamp','status']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','title', 'description', 'display_pic', 'room_stream_details', 'organization']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username', 'email', 'first_name', 'last_name']