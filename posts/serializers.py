from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')
    is_post_owner = serializers.SerializerMethodField()

    def get_is_post_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'caption', 'owner', 'is_post_owner',
            'uploaded_at', 'updated_at', 'post_image', 'profile_id', 'profile_image',
        ]
