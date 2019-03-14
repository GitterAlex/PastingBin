#models.py
from django.db import models
from django.urls import reverse
import datetime
import uuid
from django.utils.crypto import get_random_string
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import User
# Create your models here.

class PostTable(models.Model):
    postID = models.CharField(max_length=8, primary_key=True, default=get_random_string(8).lower(), help_text="Unique ID for this post")
    title =  models.CharField(max_length=100)
    expiry = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #postshares = models.ManyToManyField(User, blank=True, related_name='postshares')
    private = models.BooleanField(default=0)
    pasteContent = models.CharField(max_length=2000)

    def __str__(self):
        return self.title
