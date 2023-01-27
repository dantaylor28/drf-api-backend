from django.contrib.auth.models import User
from .models import Pin
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PinListViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')

    def test_list_all_pins(self):
        dan = User.objects.get(username='dan')
        test = Post.objects.create(owner=dan, title='dans post')
        Pin.objects.create(owner=dan, post=test)
        response = self.client.get('/pins/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
