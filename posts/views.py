from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from posts.serializers import PostSerializer
from posts.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
