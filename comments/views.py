from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from comments.serializers import CommentSerializer, CommentCreateSerializer, CommentManagementSerializer
from comments.models import Comment
from posts.models import Post

User = get_user_model()


class CommentFilteredByPost(generics.ListAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id') 
        return Comment.objects.filter(post=post_id).filter(display=True)


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        return serializer.save(post=post, user=self.request.user)
    

class CommentsPostBySeenStatus(generics.ListAPIView):
    model = Comment
    serializer_class = CommentManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        seen_status = self.request.query_params.get('seen')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise PermissionDenied("Post not found")

        if self.request.user != post.writer:
            raise PermissionDenied("You do not have permission to view these comments.")

        queryset = Comment.objects.filter(post=post_id)

        if seen_status is not None:
            seen_status = seen_status.lower() == 'true'
            queryset = queryset.filter(seen=seen_status)

        return queryset
