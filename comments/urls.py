from rest_framework.routers import DefaultRouter
from django.urls import path, include
from comments.views import CommentFilteredByPost

urlpatterns = [
    path('comments-filtered-by-post/<int:post_id>/', CommentFilteredByPost.as_view(), name="comment-filtered-by-post"),
]
