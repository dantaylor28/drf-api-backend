from rest_framework import serializers
from .models import CommentLike
from django.db import IntegrityError


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    The comment_text field displays the comment text. An integrity
    error is raised if an attempt is made to like a comment more
    than one time.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    comment_text = serializers.ReadOnlyField(source='comment.text')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'you cannot like a comment more than once'
            })

    class Meta:
        model = CommentLike
        fields = [
            'id', 'owner', 'comment', 'comment_text',
            'timestamp'
        ]
