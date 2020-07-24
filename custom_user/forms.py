from django import forms


class SignUp(forms.Form):
    name = forms.CharField(max_length=255, min_length=3, required=True, label='Name')
    email = forms.EmailField(max_length=155, required=True,label='Email')