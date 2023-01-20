from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'caption', 'owner', 'uploaded_at',
            'updated_at', 'post_image', 'profile_id', 'profile_image',
        ]
