from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models. CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Post(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users_liked = models.ManyToManyField(User, related_name='liked_posts')


