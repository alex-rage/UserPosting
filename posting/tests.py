from django.test import TestCase
from django.urls import reverse
from .models import *
from datetime import datetime



class MainTests(TestCase):
    passed_str = 'Test text. Test passed'

    def test_post_api(self):
        user = User.objects.create_user(username='tempuser', password='12345678')
        user_id = user.id
        self.client.force_login(user=user)
        response = self.client.post(reverse('post-create-view'), {'author': user_id, 'text': self.passed_str})
        self.assertIn(self.passed_str, str(response.content))
        posts_list = Post.objects.filter(text=self.passed_str)
        self.assertTrue(posts_list.exists())

        post = posts_list.first()
        post_id = post.id

        self.client.put(reverse('post-update-view', args=[post_id]),
                        {'author': user_id, 'text': self.passed_str,
                         'liked': [{'id': user_id}], 'date': datetime.now()},
                        content_type='application/json')

        self.assertIn(user, post.liked.all())

        self.client.put(reverse('post-update-view', args=[post_id]),
                        {'author': user_id, 'text': self.passed_str,
                         'liked': [], 'date': datetime.now()},
                        content_type='application/json')

        self.assertNotIn(user, post.liked.all())






