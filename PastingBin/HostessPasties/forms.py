from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PostTable
import datetime
class AccountCreation(UserCreationForm):

        username = forms.CharField(max_length=32)
        email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
        first_name = forms.CharField(max_length=50)
        last_name = forms.CharField(max_length=50)
class Meta:
    model = User
    fields = ('username','email','first_name','last_name')

class PostCreation(forms.ModelForm):
    pasteContent = forms.CharField(widget=forms.Textarea)
    expiry = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = PostTable
        fields = ('title','expiry','private','pasteContent')
