from django import forms
from .models import Room

class CreateRoom(forms.Form):
    title = forms.CharField(max_length=512, required=True,label='Room Name ')
    description = forms.CharField(max_length=1024, widget=forms.Textarea,label='Description')


class EditRoom(forms.Form):
    title = forms.CharField(max_length=512, required=True, label='Room Name')
    description = forms.CharField(max_length=1024, widget=forms.Textarea, label='Description')
    picture = forms.ImageField(required=False)



    '''organization = models.ForeignKey()
    room_number = models.IntegerField(unique=True)
    display_pic = models.ImageField(blank=True, default=None, null=True)
    room_stream_details = models.CharField(max_length=1024, default='free', blank=False, null=False)'''