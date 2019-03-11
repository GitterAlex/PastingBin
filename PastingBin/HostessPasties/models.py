from django.db import models
from django.urls import reverse
import datetime
import uuid
from django.contrib.auth.models import User
# Create your models here.

class PostTable(models.Model):
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this post")
    expiry = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=0)
    pasteContent = models.CharField(max_length=2000)
