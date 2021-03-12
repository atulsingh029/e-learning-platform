"""
author   : github.com/atulsingh029
added in : version 2.0.0
"""
# this file contains required model classes to store in the data structure


class CacheUser:
    def __init__(self, obj):
        if obj.is_organization:
            usertype = 'organization'
            type_obj = obj.organization
        elif obj.is_teacher:
            usertype = 'teacher'
            type_obj = obj.teacher
        else:
            usertype = 'student'
            type_obj = obj.student
        self.id = obj.id
        self.username = obj.username
        self.first_name = obj.first_name
        self.last_name = obj.last_name
        self.email = obj.email
        self.phone = obj.phone
        self.usertype = usertype
        self.usertype_obj = type_obj
        self.bio1 = obj.bio1
        self.bio2 = obj.bio2
        self.sex = obj.sex
        self.url = obj.url
        self.profile_pic = obj.profile_pic

    def __str__(self):
        return self.username