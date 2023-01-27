from django.contrib.auth.models import User
from .models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class CategoryListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='dan', password='password1')

    def test_list_all_categories(self):
        dan = User.objects.get(username='dan')
        Category.objects.create(name='food')
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_can_make_category(self):
        self.client.login(username='dan', password='password1')
        response = self.client.post('/categories/', {'name': 'food'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
