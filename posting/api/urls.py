from . import views
from django.urls import path
from rest_framework_simplejwt.views import *


urlpatterns = [
    path('posts-list/', views.PostListView.as_view(), name='posts-list'),
    path('posts-request/', views.posts_request, name='posts-request'),
    path('post-create-view/', views.PostCreateAPIView.as_view(), name='post-create-view'),
    path('create-post-request/', views.create_post_request, name='create-post-request'),
    path('like-unlike-post-request/<int:post_id>/', views.like_unlike_post_request, name='like-unlike-post-request'),
    path('post-update-view/<int:pk>/', views.PostUpdateView.as_view(), name='post-update-view'),
    path('user-list-view/<int:pk>/', views.UserListView.as_view(), name='user-list-view'),
    path('post-retrieve-view/<int:pk>/', views.PostRetrieveView.as_view(), name='post-retrieve-view'),
    path('user-retrieve-view/<int:pk>/', views.UserRetrieveView.as_view(), name='user-retrieve-view'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('token-sliding/', TokenObtainSlidingView.as_view(), name='token-sliding'),
    path('token-refresh/', TokenRefreshSlidingView.as_view(), name='token-sliding-refresh'),
    path('api-login/', views.api_login, name='api-login'),
    path('', views.api_login, name='api-index')
    ]

