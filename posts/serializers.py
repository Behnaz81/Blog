from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Post, Category

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')
        read_only_field = ('id')


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b")
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'category', 'writer', 'created_at', 'updated_at', 'image')
        read_only_field = ('id', 'writer', 'created_at', 'updated_at')


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'category', 'image')
        read_only_field = ('id',)


        