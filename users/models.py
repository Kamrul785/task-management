from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_image',
        blank=True,
        default='profile_image/default.png'
    )
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
    
