from django import forms


class AddBook(forms.Form):
    title = forms.CharField(max_length=125, required=True, label='Title')
    description = forms.CharField(max_length=512, required=False, label='Description')
    cover_pic = forms.ImageField(required=False,label='Select A Book Cover',)
    type = forms.ChoiceField(choices=[('academic','academic'),('non-academic','non-academic')], label="Book Type")
    file = forms.FileField(label='Upload PDF Book', required=True)
    author = forms.CharField(max_length=125, required=True, label='Author')
    edition = forms.CharField(max_length=125, required=True, label='Edition')
    publisher = forms.CharField(max_length=125, required=True, label='Publisher')