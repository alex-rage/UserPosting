from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from datetime import datetime
from rest_framework.decorators import permission_classes




@permission_classes(('AllowAny',))
def test_post_api():
    user = User.objects.create_user(username='tempuser', password='12345678')
    client = Client()
    user_id = user.id
    passed_str = 'Test text. Test passed'
    response = client.post(reverse('post-create-view'), {'author': user_id, 'text': passed_str})
    assert (passed_str in str(response.content))
    posts_list = Post.objects.filter(text=passed_str)
    assert (posts_list.exists == True)
    post = posts_list.first()
    post_id = post.id

    json_data = {'author': user_id, 'text': passed_str,
                'liked': [{'id': user_id}], 'date': datetime.now()}

    client.put(reverse('post-update-view', args=[post_id]), json_data, content_type='application/json')

    assert (user in post.liked.all())

    json_data['liked'] = []

    client.put(reverse('post-update-view', args=[post_id]), json_data, content_type='application/json')

    assert (user not in post.liked.all())






