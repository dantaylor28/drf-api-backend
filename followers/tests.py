from django.contrib.auth.models import User
from .models import Follower
from rest_framework import status
from rest_framework.test import APITestCase


class FollowerListViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')

    def test_list_all_followers(self):
        dan = User.objects.get(username='dan')
        sabina = User.objects.get(username='sabina')
        follow = Follower.objects.create(owner=dan, followed=sabina)
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
