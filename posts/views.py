from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.serializers import PostSerializer, CategorySerializer, PostCreateSerializer
from posts.models import Post, Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostFilteredByCategory(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id') 
        return Post.objects.filter(category=cat_id)


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)
    

class ListPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class RetrievePostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
