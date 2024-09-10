from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.message} by {self.user} for {self.post}'
    

    class Meta:
        ordering = ['-posted_at']
