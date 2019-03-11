from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AccountCreation(UserCreationForm):

        username = forms.CharField(max_length=32)
        email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
        first_name = forms.CharField(max_length=50)
        last_name = forms.CharField(max_length=50)
class Meta:
    model = User
    fields = ('username','password','email','first_name','last_name')
