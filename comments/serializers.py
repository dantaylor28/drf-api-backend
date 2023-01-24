from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')
    post_title = serializers.ReadOnlyField(source='post.title')
    is_comment_owner = serializers.SerializerMethodField()

    def get_is_comment_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'text', 'owner',
            'is_comment_owner', 'timestamp', 'updated_at',
            'profile_id', 'profile_image'
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    This serializer is only necessary to autofill the post field that
    we are editing to save users from having to reselect the corresponding
    post every time
    """
    post = serializers.ReadOnlyField(source='post.id')
