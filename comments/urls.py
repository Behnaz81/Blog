from rest_framework.routers import DefaultRouter
from django.urls import path, include
from comments.views import CommentFilteredByPost, CreateCommentView, CommentsPostBySeenStatus, CommentsDisplayView

urlpatterns = [
    path('comments-filtered-by-post/<int:post_id>/', CommentFilteredByPost.as_view(), name="comment-filtered-by-post"),
    path('comment-add/<int:post_id>/', CreateCommentView.as_view(), name="add-comment"),
    path('comments-seen-status/<int:post_id>/', CommentsPostBySeenStatus.as_view(), name="comments-seen-status"),
    path('comments-display/<int:comment_id>/', CommentsDisplayView.as_view(), name="display-comment"),
]
