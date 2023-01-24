from django.shortcuts import render
from .models import Follower
from .serializers import FollowerSerializer
from rest_framework import generics


class FollowerListView(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all().order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
