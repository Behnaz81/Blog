from rest_framework import serializers 
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    posted_at = serializers.DateTimeField(format="%d %b")

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'message', 'seen', 'display', 'posted_at')
        read_only_fields = ('id', 'posted_at')
