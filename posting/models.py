from django.db import models
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', default=None)
    text = models.TextField(max_length=1000, default='')
    date = models.DateTimeField(default=datetime.datetime.now)
    liked = models.ManyToManyField(User, default=None)

