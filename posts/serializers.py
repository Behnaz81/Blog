from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'category', 'writer', 'created_at', 'updated_at')
        read_only_field = ('id', 'writer', 'created_at', 'updated_at')