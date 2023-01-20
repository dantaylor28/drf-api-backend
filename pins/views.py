from django.shortcuts import render
from .models import Pin
from .serializers import PinSerializer
from rest_framework import generics


class PinListView(generics.ListCreateAPIView):
    serializer_class = PinSerializer
    queryset = Pin.objects.all().order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
