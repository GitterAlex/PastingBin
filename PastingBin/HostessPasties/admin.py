#admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PostTable

#register post table to admin page 
admin.site.register(PostTable)
