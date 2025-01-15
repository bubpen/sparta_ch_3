from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length = 300, null= True, default='안녕하세요')
    image = models.ImageField()
    
    def __str__(self):
        return self.username
