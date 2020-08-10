from rest_framework import serializers
from custom_user.models import ApplyForStudent, Room, Account
from management.models import Course, Lecture, CourseResource, LectureResource


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForStudent
        fields = ['id','first_name','last_name','email','phone','reference','submissionstamp','status']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','title', 'description', 'display_pic', 'room_stream_details', 'organization']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username', 'email', 'first_name', 'last_name']


# @abhishek
# write serializers for following models :
        '''
        NamingConvention for class name --> ClassNameThatYouAreSerializingSerializer
        
        custom_user --> Account (some important ones are already added, add other fields)
        management --> Course, CourseResources, Lecture, LectureResources
        
        note: add only those fields that are relevant to show on front end, don't add sensitive fields like password
        '''