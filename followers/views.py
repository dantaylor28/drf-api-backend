from django.shortcuts import render
from .models import Follower
from .serializers import FollowerSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics


class FollowerListView(generics.ListCreateAPIView):
    """
    Lists all instances where a user follows another user.
    Authenticated users can follow a profile using the form.
    """
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all().order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetailView(generics.RetrieveDestroyAPIView):
    """
    Retrieves a single user following result. This can be deleted
    if you are signed in as the owner of the follow.
    """
    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
