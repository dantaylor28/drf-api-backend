from django.contrib.auth.models import User
from .models import CommentLike, Comment
from posts.models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentLikeListViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')

    def test_list_all_comment_likes(self):
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        comment1 = Comment.objects.create(owner=dan, post=post1)
        CommentLike.objects.create(owner=dan, comment=comment1)
        response = self.client.get('/comments/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_out_cannot_like_comment(self):
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        comment1 = Comment.objects.create(owner=dan, post=post1)
        response = self.client.post(
            '/comments/likes/', {'comment': 'comment1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentLikeDetailViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')
        post1 = Post.objects.create(owner=dan, title='dans post')
        post2 = Post.objects.create(owner=sabina, title='sabinas post')
        comment1 = Comment.objects.create(owner=dan, post=post2, text='hi')
        comment2 = Comment.objects.create(owner=sabina, post=post1, text='bye')
        CommentLike.objects.create(owner=dan, comment=comment2)
        CommentLike.objects.create(owner=sabina, comment=comment1)

    def test_get_comment_like_by_id(self):
        response = self.client.get('/comments/likes/1')
        self.assertEqual(response.data['comment_text'], 'bye')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existant_comment_like_id(self):
        response = self.client.get('comments/likes/32')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_comment_like(self):
        self.client.login(username='dan', password='password1')
        response = self.client.delete('/comments/likes/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_others_comment_like(self):
        self.client.login(username='dan', password='password1')
        response = self.client.delete('/comments/likes/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
