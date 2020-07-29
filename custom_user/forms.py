from django import forms


class SignUp(forms.Form):
    name = forms.CharField(max_length=255, min_length=3, required=True, label='Name')
    email = forms.EmailField(max_length=155, required=True,label='Email')
    password1 = forms.CharField(max_length=512,widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=512, widget=forms.PasswordInput, label='Confirm Password')


class OTPForm(forms.Form):
    otp = forms.CharField(min_length=6,max_length=6,label='Verify One Time Password ')