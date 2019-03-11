#admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PostTable
# Register your models here.

class AccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(PostTable)
