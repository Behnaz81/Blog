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
    image = models.ImageField(upload_to="images", default="images/default-post.png")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title
