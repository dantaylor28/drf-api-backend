from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment
from comment_likes.models import CommentLike


class CommentSerializer(serializers.ModelSerializer):
    """
    Multiple extra fields have been added including the post title,
    a boolean on whether the current user is the comment owner. Functions
    are present to display date and time in a more user friendly
    format.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')
    post_title = serializers.ReadOnlyField(source='post.title')
    is_comment_owner = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    num_of_comment_likes = serializers.ReadOnlyField()
    comment_liked_id = serializers.SerializerMethodField()

    def get_comment_liked_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            comment_like = CommentLike.objects.filter(
                owner=user, comment=obj
            ).first()
            return comment_like.id if comment_like else None
        return None

    def get_is_comment_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_timestamp(self, obj):
        return naturaltime(obj.timestamp)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'text', 'num_of_comment_likes',
            'owner', 'is_comment_owner', 'timestamp', 'updated_at',
            'profile_id', 'profile_image', 'comment_liked_id'
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    This serializer is only necessary to autofill the post field that
    we are editing to save users from having to reselect the corresponding
    post every time
    """
    post = serializers.ReadOnlyField(source='post.id')
