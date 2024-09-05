from rest_framework import viewsets
from rest_framework import generics
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


class PostFilteredByCategory(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id') 
        return Post.objects.filter(category=cat_id)
