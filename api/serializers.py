from rest_framework import serializers
from custom_user.models import ApplyForStudent, Room, Account, Student, Teacher
from management.models import Course, Lecture, CourseResource, DashOption
from elibrary.models import Book, BookReview, TextReviews
from management.models import Assignment, Solution, Slot


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForStudent
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'reference', 'submissionstamp', 'status']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'description', 'display_pic', 'room_stream_details', 'organization', 'reference']
        depth = 1


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phone', 'profile_pic']


class StudentSerializer(serializers.ModelSerializer):
    user = AccountSerializer()
    from_room = RoomSerializer()
    class Meta:
        model = Student
        fields = ['id', 'from_room', 'from_organization', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    user = AccountSerializer()
    class Meta:
        model = Teacher
        fields = ['id','user']


class CustomInstructor(serializers.ModelSerializer):
    user = AccountSerializer()
    class Meta:
        model = Teacher
        fields = ['user',]


class CourseSerializer(serializers.ModelSerializer):
    instructor = CustomInstructor()
    class Meta:
        model = Course
        fields = ['c_id', 'c_name', 'c_description', 'for_organization', 'c_status', 'instructor']



class CourseSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['c_id', 'c_name', 'c_description', 'for_organization', 'c_status']


class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['id', 'cr_name', 'cr_description', 'file', 'cr_url', ]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'for_course', 'l_number', 'l_name', 'video', 'l_description']



class DashOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashOption
        fields = ['link', 'label', 'icon', 'method']


class CustomStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=1024)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(max_length=1024)
    room = serializers.CharField(max_length=1024)
    phone = serializers.IntegerField()


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['points', 'reviews']


class BookSerializer(serializers.ModelSerializer):
    bookreview = BookReviewSerializer()
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'type', 'edition', 'publisher', 'file', 'cover', 'bookreview']


class TextReviewSerializer(serializers.ModelSerializer):
    reviewer = AccountSerializer()
    class Meta:
        model = TextReviews
        fields = ['text', 'reviewer']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'name', 'description', 'for_course', 'max_marks', 'problem']


class SolutionSerializer(serializers.ModelSerializer):
    uploader = AccountSerializer()
    class Meta:
        model = Solution
        fields = ['id', 'uploader', 'solution_to', 'solution', 'marks', 'remarks', 'uploader']


class SlotSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Slot
        fields = ['id', 'course', 'start_time', 'session_id', 'agenda', 'date']