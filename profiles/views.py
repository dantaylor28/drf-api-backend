from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().order_by('-created_at')


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
