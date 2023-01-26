from rest_framework import serializers
from .models import Follower
from django.db import IntegrityError


class FollowerSerializer(serializers.ModelSerializer):
    """
    The followed user's username has been included as an extra
    field along with the create method to ensure you cannot follow
    yourself or other users more than once.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_user = serializers.ReadOnlyField(source='followed.username')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error':
                'you cannot follow yourself or other users more than once'
            })

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'followed', 'followed_user',
            'timestamp'
        ]
