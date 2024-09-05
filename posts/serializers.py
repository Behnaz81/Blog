from rest_framework import serializers
from posts.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'category', 'writer', 'created_at', 'updated_at', 'image')
        read_only_field = ('id', 'writer', 'created_at', 'updated_at')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')
        read_only_field = ('id')
        