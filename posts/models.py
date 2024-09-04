from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)

    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
    
    
class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
