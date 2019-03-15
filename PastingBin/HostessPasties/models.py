#models.py
from django.db import models
from django.urls import reverse
import datetime
import uuid
from django.utils.crypto import get_random_string
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import User
from django.db import IntegrityError
from fernet_fields import EncryptedTextField
# Create your models here.

class PostTable(models.Model):
    postID = models.CharField(max_length=8, primary_key=True, help_text="Unique ID for this post")
    title =  models.CharField(max_length=100)
    expiry = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    postshares = models.ManyToManyField(User, blank=True, related_name='postshares')
    private = models.BooleanField(default=0)
    pasteContent = EncryptedTextField(default='')

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        content = file.render_text_content()
        return HttpResponse(content, content_type='text/plain; charset=utf8')

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
