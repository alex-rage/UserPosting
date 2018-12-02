from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_authenticated = True
    else:
        user_id = None
        user_authenticated = False

    liked_posts_ids = []

    posts = Post.objects.all()

    for post in posts:
        all_post_likes = post.liked.all()
        if all_post_likes.filter(id=user_id).exists():
            liked_posts_ids.append(post.id)

    return render(request, 'index.html', {'posts': posts,
                                          'user_id': user_id,
                                          'user_authenticated': user_authenticated,
                                          'liked_posts_ids': liked_posts_ids})



@login_required(redirect_field_name=None)
def create_post(request):
    user = request.user
    user_id = request.user.id

    post = Post()
    post.author = user
    author_name = user.username


    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid:
            post_form.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        post_form = PostForm()

    return render(request, 'create_post.html', {'post_form': post_form,
                                                'user_id': user_id,
                                                'author_name': author_name})


def sign_up(request):
    if request.method == 'POST':
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        sign_up_form = UserCreationForm()

    return render(request, 'sign-up.html', {'sign_up_form': sign_up_form})

@login_required(redirect_field_name=None)
@require_POST
def like_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    if not user in post.liked.all():
        post.liked.add(user)
        post.save()

    return HttpResponseRedirect(reverse('index'))


@login_required(redirect_field_name=None)
@require_POST
def unlike_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    if user in post.liked.all():
        post.liked.remove(user)
        post.save()

    return HttpResponseRedirect(reverse('index'))
