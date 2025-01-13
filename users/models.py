from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(max_length = 200, null = True, blank = True)

