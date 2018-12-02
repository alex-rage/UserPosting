from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests, json
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.generics import *
from .serializers import *


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostRetrieveView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer


class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def get_token_headers(request):
    jwt_token = request.COOKIES.get('token')

    if jwt_token is None:
        return None

    headers = {'Authorization': 'Bearer ' + jwt_token}
    return headers


def get_view_full_url(request, view_name, args=None):
    url = request.build_absolute_uri(location=reverse(view_name, args=args))
    return url


@login_required(redirect_field_name=None)
def create_post_request(request):
    user_id = request.user.id
    headers = get_token_headers(request)
    if headers is None:
        return HttpResponseRedirect(reverse('api-login'))
    post_url = get_view_full_url(request, 'post-create-view')
    response = requests.post(post_url, headers=headers, json={'author': user_id, 'text': 'Hello', 'liked': []})
    return HttpResponse(response.content)


def posts_request(request):
    headers = get_token_headers(request)
    if headers is None:
        return HttpResponseRedirect(reverse('api-login'))

    posts_url = get_view_full_url(request, 'posts-list')
    response = requests.get(posts_url, headers=headers)
    return HttpResponse(response.content)


@login_required(redirect_field_name=None)
def like_unlike_post_request(request, post_id):
    user = request.user
    user_id = user.id
    headers = get_token_headers(request)
    if headers is None:
        return HttpResponseRedirect(reverse('api-login'))

    post_url = get_view_full_url(request, 'post-retrieve-view', args=[post_id])
    response = requests.get(post_url, headers=headers)
    post_json = json.loads(response.text)
    liked_list = post_json.get('liked')
    if liked_list is None:
        return HttpResponse(str(post_json))

    user_like_json = {"id": user_id}

    if user_like_json in liked_list:
        liked_list.remove(user_like_json)
    else:
        liked_list.append(user_like_json)

    post_json['liked'] = liked_list

    update_post_url = get_view_full_url(request, 'post-update-view', args=[post_id])
    response = requests.put(update_post_url, headers=headers, json=post_json)

    return HttpResponse(response.text)


def api_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                return HttpResponse('Failed to authenticate')

            login(request, user)

            token_url_path = reverse('token-sliding')
            token_api_url = request.build_absolute_uri(location=token_url_path)
            response = requests.post(token_api_url, data={'username': username, 'password': password})
            jwt_token_dict = response.json()
            jwt_token = jwt_token_dict['token']
            if not jwt_token:
                return HttpResponse('Failed to generate token')

            else:
                response = HttpResponseRedirect(reverse('index'))
                response.set_cookie('token', jwt_token)
                return response

    else:
        form = AuthenticationForm()

    return render(request, 'api-login.html', {'form': form})