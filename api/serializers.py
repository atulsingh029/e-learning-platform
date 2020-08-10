from rest_framework import serializers
from custom_user.models import ApplyForStudent, Room, Account
from management.models import Course, Lecture, CourseResource, LectureResource


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForStudent
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'reference', 'submissionstamp', 'status']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'description', 'display_pic', 'room_stream_details', 'organization']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['c_id', 'c_name', 'c_description', 'for_organization', 'c_status']


class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['cr_name', 'cr_description', 'for_course', 'cr_url']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['for_course', 'l_number', 'l_name', 'l_url']


class LectureResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureResource
        fields = ['lr_name', 'lr_description', 'for_lecture', 'lr_url']

# @abhishek
# write serializers for following models :
        '''
        NamingConvention for class name --> ClassNameThatYouAreSerializingSerializer
        
        custom_user --> Account (some important ones are already added, add other fields)
        management --> Course, CourseResources, Lecture, LectureResources
        
        note: add only those fields that are relevant to show on front end, don't add sensitive fields like password
        '''