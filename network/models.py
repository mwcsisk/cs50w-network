from django.contrib.auth.models import AbstractUser
from django.db import models
from pytz import timezone


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', editable=False)
    body = models.CharField(max_length=240)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked")

    posts = models.Manager()

    def serialize(self):
        usw_tz = timezone('America/Los_Angeles')
        timestamp = self.timestamp.astimezone(usw_tz)

        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": timestamp.strftime("%b. %#d, %Y, %#I:%M %p"),
            "num_likes": self.likes.all().count()
        }