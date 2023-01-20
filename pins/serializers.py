from rest_framework import serializers
from .models import Pin
from django.db import IntegrityError


class PinSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'you cannot pin a post more than once'
            })

    class Meta:
        model = Pin
        fields = [
            'id', 'owner', 'post', 'post_title',
            'timestamp'
        ]
