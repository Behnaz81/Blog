from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ADMIN_USER = 1
    SIMPLE_USER = 2

    ROLE_CHOICES = (
        ('Admin User', ADMIN_USER),
        ('Simple User', SIMPLE_USER)
    )

    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='Simple User')
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='images', default='images/default-user.png')
