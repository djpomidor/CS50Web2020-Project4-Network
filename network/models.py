from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #id = models.AutoField(primary_key=True)
    followers =  models.CharField(max_length=64)
    def __str__(self):
        return f"{self.username}"

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.CharField(max_length=64)
