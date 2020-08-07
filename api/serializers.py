from rest_framework import serializers
from custom_user.models import ApplyForStudent, Room
from django.contrib.auth.admin import User


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForStudent
        fields = ['first_name','last_name','email','phone','reference','submissionstamp']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['title', 'description', 'display_pic', 'room_stream_details', 'organization']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']