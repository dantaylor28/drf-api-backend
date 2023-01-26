from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')

    def test_update_own_profile(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/profiles/1', {'location': 'sweden'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.location, 'sweden')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_others_profile(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/profiles/2', {'location': 'sweden'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
