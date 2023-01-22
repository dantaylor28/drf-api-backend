from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'text', 'owner',
            'timestamp', 'updated_at', 'profile_id',
            'profile_image'
        ]
