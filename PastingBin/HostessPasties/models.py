#models.py
from django.db import models
from django.urls import reverse
import datetime
import uuid
from django.utils.crypto import get_random_string
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import User
from django.db import IntegrityError
# Requires pip install django-fernet-fields
from fernet_fields import EncryptedTextField
#Posttable model
class PostTable(models.Model):
    #id of the post is a random 8 character string and is the primary key
    postID = models.CharField(max_length=8, primary_key=True, help_text="Unique ID for this post")
    #title field
    title =  models.CharField(max_length=100)
    #post expiry field date
    expiry = models.DateField(default=datetime.date.today)
    #owner field should be the same as user id
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #many users can share many posts, creates a table with link between user and post id
    postshares = models.ManyToManyField(User, blank=True, related_name='postshares')
    #checks if post is private 
    private = models.BooleanField(default=0)
    #enrypts content
    pasteContent = EncryptedTextField(default='')
    #allows to make posts without overwriting
    def save(self, *args, **kwargs):
        if not self.postID:
            self.postID = get_random_string(8)
        success = False
        errors = 0
        while not success:
            try:
                super(PostTable, self).save(*args, **kwargs)
            except IntegrityError:
                errors += 1
                if errors > 3:
                    # tried 3 times, no dice. raise the integrity error and handle elsewhere
                    raise
                else:
                    self.code = get_random_string(8)
            else:
                success = True

    def __str__(self):
        return self.title
