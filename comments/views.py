from rest_framework import generics
from django.contrib.auth import get_user_model
from comments.serializers import CommentSerializer, CommentCreateSerializer
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

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        user = User.objects.get(id=1)
        return serializer.save(post=post, user=user)