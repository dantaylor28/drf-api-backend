from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_profile_owner = serializers.SerializerMethodField()

    def get_is_profile_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'location', 'bio', 'owner',
            'is_profile_owner', 'created_at', 'updated_at',
            'profile_image',

        ]
