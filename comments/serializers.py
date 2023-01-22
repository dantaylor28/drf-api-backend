from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'text', 'owner',
            'timestamp', 'updated_at', 'profile_id',
            'profile_image'
        ]