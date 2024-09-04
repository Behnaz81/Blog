from rest_framework import viewsets
from django.shortcuts import render
import requests
from posts.serializers import PostSerializer, CategorySerializer
from posts.models import Post, Category


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def index_view(request):
    posts_get = requests.get('http://localhost:8000/api/posts/')
    posts = posts_get.json()
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)
