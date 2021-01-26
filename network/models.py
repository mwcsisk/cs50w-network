from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    users = models.Manager()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', editable=False)
    body = models.CharField(max_length=240)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked")

    posts = models.Manager()