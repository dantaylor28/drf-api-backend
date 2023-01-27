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

    def test_logged_out_cannot_pin(self):
        dan = User.objects.get(username='dan')
        post = Post.objects.create(owner=dan, title='dans post')
        response = self.client.post('/pins/', {'post': 'post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PinDetailViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')
        post1 = Post.objects.create(owner=dan, title='dans post')
        post2 = Post.objects.create(owner=sabina, title='sabinas post')
        Pin.objects.create(owner=dan, post=post1)
        Pin.objects.create(owner=sabina, post=post2)

    def test_get_pin_by_id(self):
        response = self.client.get('/pins/1')
        self.assertEqual(response.data['post'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existant_pin_id(self):
        response = self.client.get('pins/32')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('posts/32')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_pin(self):
        self.client.login(username='dan', password='password1')
        response = self.client.delete('/pins/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
