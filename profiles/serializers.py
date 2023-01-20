from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'location', 'bio', 'owner',
            'created_at', 'updated_at', 'profile_image',

        ]
