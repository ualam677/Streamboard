from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_dark = models.BooleanField(default=False)

    def __str__(self):
        return self.username
