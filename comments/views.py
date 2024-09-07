from rest_framework import generics
from comments.serializers import CommentSerializer
from comments.models import Comment


class CommentFilteredByPost(generics.ListAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id') 
        return Comment.objects.filter(post=post_id).filter(display=True)
