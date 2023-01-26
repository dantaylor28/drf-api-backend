from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics, filters


class ProfileListView(generics.ListAPIView):
    """
    Lists out all users and their profile information.
    Profiles can be filtered, searched and ordered from
    a number of options.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        num_of_posts=Count('owner__post', distinct=True),
        num_of_followers=Count('owner__followed', distinct=True),
        num_of_following=Count('owner__following', distinct=True),
        num_of_pinned_posts=Count('owner__pin', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]

    search_fields = [
        'owner__username',
        'owner__profile__name',
        'owner__profile__location'
    ]

    ordering_fields = [
        'num_of_followers',
        'num_of_following',
        'num_of_posts'
    ]

    filterset_fields = [
        # shows profiles that are following the selected user
        'owner__following__followed__profile',
        # shows profiles that are followed by the selected user
        'owner__followed__owner__profile'
    ]


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists all information for a selected user and the ability to edit
    and delete the profile if you are the owner
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        num_of_posts=Count('owner__post', distinct=True),
        num_of_followers=Count('owner__followed', distinct=True),
        num_of_following=Count('owner__following', distinct=True),
        num_of_pinned_posts=Count('owner__pin', distinct=True)
    ).order_by('-created_at')
