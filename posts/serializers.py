from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Post
from pins.models import Pin


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.profile_image.url')
    is_post_owner = serializers.SerializerMethodField()
    pinned_id = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.name')
    num_of_pins = serializers.ReadOnlyField()
    num_of_comments = serializers.ReadOnlyField()

    def validate_post_image(self, value):
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

    def get_is_post_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_pinned_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            pin = Pin.objects.filter(
                owner=user, post=obj
            ).first()
            return pin.id if pin else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'caption', 'owner', 'is_post_owner',
            'category', 'category_name', 'uploaded_at', 'updated_at',
            'post_image', 'profile_id', 'profile_image', 'pinned_id',
            'num_of_pins', 'num_of_comments'
        ]
