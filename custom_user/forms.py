from django import forms


class SignIn(forms.Form):
    email = forms.EmailField(max_length=155,required=True,label='Email')
    password = forms.CharField(max_length=512,widget=forms.PasswordInput,label='Password')


class SignUp(forms.Form):
    name = forms.CharField(max_length=255, min_length=3, required=True, label='Name')
    email = forms.EmailField(max_length=155, required=True,label='Email')
    password1 = forms.CharField(max_length=512,widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=512, widget=forms.PasswordInput, label='Confirm Password')


class OTPForm(forms.Form):
    otp = forms.CharField(min_length=6,max_length=6,label='Verify One Time Password ')


class StudentRegister(forms.Form):
    first_name = forms.CharField(max_length=512, required=True, label='First Name ')
    last_name = forms.CharField(max_length=512, label='Last Name ')
    email = forms.EmailField(max_length=512, required=True, label='Email')
    phone = forms.CharField(min_length=10,max_length=10, label='Phone Number',)
    password1 = forms.CharField(max_length=512, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=512, widget=forms.PasswordInput, label='Confirm Password')