from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    name = models.CharField(max_length=150)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User,related_name="watchlist", blank=True)
    
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="listings")
    imageurl = models.CharField(max_length=600, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    closed = models.BooleanField(default=False)

    description = models.CharField(max_length=600)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.author}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="biddings")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.price} bid on {self.listing.name} by {self.author}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=600)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="comments")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.listing.name} by {self.author}"

