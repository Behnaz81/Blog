from rest_framework import serializers 
from posts.serializers import PostSerializer
from users.serializers import UserSerializer
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    posted_at = serializers.DateTimeField(format="%d %b")
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'message', 'seen', 'display', 'posted_at')
        read_only_fields = ('id', 'posted_at', 'post', 'seen', 'display')


class CommentCreateSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'message')
        read_only_fields = ('id', 'post', 'user')


class CommentManagementSerializer(serializers.ModelSerializer):
    posted_at = serializers.DateTimeField(format="%d %b")
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'message', 'seen', 'display', 'posted_at')
        read_only_fields = ('id', 'posted_at', 'post', 'seen', 'display')