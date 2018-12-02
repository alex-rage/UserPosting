from rest_framework.serializers import ModelSerializer
from django.shortcuts import get_object_or_404
from posting.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }


class PostSerializer(ModelSerializer):
    liked = UserSerializer(many=True, allow_null=True)
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        post = Post()
        post.author = validated_data['author']
        post.text = validated_data['text']
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.author = validated_data['author']
        instance.text = validated_data['text']
        instance.date = validated_data['date']

        liked_data = validated_data.pop('liked')
        likes_list = []
        for like in liked_data:
            user_id = like['id']
            like_obj = get_object_or_404(User, id=user_id)
            likes_list.append(like_obj)

        instance.liked.set(likes_list, clear=True)

        instance.save()
        return instance

