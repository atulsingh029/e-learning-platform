from django import forms
from .models import Room
import management

class CreateRoom(forms.Form):
    title = forms.CharField(max_length=512, required=True,label='Room Name ')
    description = forms.CharField(max_length=1024, widget=forms.Textarea,label='Description')


class EditRoom(forms.Form):
    title = forms.CharField(max_length=512, required=True, label='Room Name')
    description = forms.CharField(max_length=1024, widget=forms.Textarea, label='Description')
    picture = forms.ImageField(required=False)


class AddNewTeacher(forms.Form):
    first_name = forms.CharField(max_length=512,required=True,label='First Name')
    last_name = forms.CharField(max_length=512, required=True, label='Last Name')
    email = forms.EmailField(required=True,max_length=1024,label='Email')
    phone = forms.CharField(max_length=13,label='Phone Number',required=False)
    profile_pic = forms.ImageField(required=False,label='Select A Profile Picture')
    sex = forms.ChoiceField(choices=[('male','male'),('female','female')])


class AddNewStudent(forms.Form):
    first_name = forms.CharField(max_length=512, required=True, label='First Name')
    last_name = forms.CharField(max_length=512, required=True, label='Last Name')
    email = forms.EmailField(required=True, max_length=1024, label='Email')
    phone = forms.CharField(max_length=13, label='Phone Number', required=False)
    profile_pic = forms.ImageField(required=False, label='Select A Profile Picture')
    sex = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')])

    '''organization = models.ForeignKey()
    room_number = models.IntegerField(unique=True)
    display_pic = models.ImageField(blank=True, default=None, null=True)
    room_stream_details = models.CharField(max_length=1024, default='free', blank=False, null=False)'''