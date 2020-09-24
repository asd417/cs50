from django.db import models

from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

# requires Pillow Library
# pip install Pillow

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Recipe(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="recipes", default=None, null=True, blank=True)
    title = models.CharField(max_length=200, default='')
    stepCount = models.IntegerField(default=0)
    liked_by = models.ManyToManyField("User", related_name="recipes_liked", blank=True)
    image = models.ImageField(upload_to ='images/', null=True, blank=True, default='NULL')

    def __str__(self):
        return f"{self.title} by {self.author}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "title": self.title,
            "liked_by": [user.username for user in self.liked_by.all()]
        }

class Step(models.Model):
    steporder = models.IntegerField(default=0)
    recipe = models.ForeignKey('Recipe', related_name='steps', on_delete=models.CASCADE, default=None, null=True, blank=True)
    content = models.CharField(max_length=300, default='')
    image = models.ImageField(upload_to ='images/', null=True, blank=True, default='NULL')
    
    def __str__(self):
        return f"Step {self.steporder + 1} of {self.recipe} with image {self.image is not None}"