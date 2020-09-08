from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="following")

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField("User", related_name="posts_liked",blank=True)

    def __str__(self):
        return f"Post by {self.author} id: {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
            "liked_by": [user.username for user in self.liked_by.all()]
        }