from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_profile_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    num_of_posts = serializers.ReadOnlyField()
    num_of_following = serializers.ReadOnlyField()
    num_of_followers = serializers.ReadOnlyField()
    num_of_pinned_posts = serializers.ReadOnlyField()

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

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'location', 'bio', 'owner',
            'is_profile_owner', 'created_at', 'updated_at',
            'profile_image', 'following_id', 'num_of_posts',
            'num_of_pinned_posts', 'num_of_followers', 'num_of_following'
        ]
