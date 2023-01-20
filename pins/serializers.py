from rest_framework import serializers
from .models import Pin


class PinSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Pin
        fields = [
            'id', 'owner', 'post', 'post_title',
            'timestamp'
        ]
