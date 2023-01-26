from django.contrib.humanize.templatetags.humanize import naturalday
from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Extra fields include the num_of_followers/following/
    posts of a user. Image validation ensures profile images
    do not exceed 2mb file size and 4096px height or width.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_profile_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    num_of_posts = serializers.ReadOnlyField()
    num_of_following = serializers.ReadOnlyField()
    num_of_followers = serializers.ReadOnlyField()
    num_of_pinned_posts = serializers.ReadOnlyField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def validate_profile_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image files cannot be larger than 2mb'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width cannot be larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height cannot be larger than 4096px'
            )
        return value

    def get_is_profile_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_updated_at(self, obj):
        return naturalday(obj.updated_at)

    def get_created_at(self, obj):
        return naturalday(obj.created_at)

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'location', 'bio', 'owner',
            'is_profile_owner', 'created_at', 'updated_at',
            'profile_image', 'following_id', 'num_of_posts',
            'num_of_pinned_posts', 'num_of_followers', 'num_of_following'
        ]
