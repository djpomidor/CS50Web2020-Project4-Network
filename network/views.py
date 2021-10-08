import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User
from network.models import *

def index(request):
    posts_list = Post.objects.all().order_by("-created")
    paginator = Paginator(posts_list, 5) # Show 5 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "header": "All posts"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(redirect_field_name='index')
def create_post(request):
    if request.method == "POST":
        post = request.POST["post"]
        new_post = Post(
            user_id = request.user.id,
            post = post)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


@login_required(redirect_field_name='index')
def user_profile(request, username):
    user_info = User.objects.get(username = username)
    user_posts = Post.objects.filter(user_id = user_info.id).order_by("-created")
    paginator = Paginator(user_posts, 5) # Show 5 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "curent_user_id": user_info.id,
        "username": username,
        "followers": user_info.followers.count(),
        "follow": user_info.follow.count(),
        "posts": posts,
        "header": "All posts from " + username
    })


@csrf_exempt
@login_required
def post_likes(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like"):
            post.unlikes.remove(data["like"])
            post.likes.add(data["like"])
        elif data.get("unlike"):
            post.likes.remove(data["unlike"])
            post.unlikes.add(data["unlike"])
        return JsonResponse({"likes_counter": post.likes_counter(), "message": "You voted for this post."}, status=201)
    return JsonResponse({"message": "PUT request required"}, status=201)


@csrf_exempt
@login_required(redirect_field_name='index')
def follow(request, user_id):
    if request.method == "PUT":
        other_user = User.objects.get(id=user_id)
        data = json.loads(request.body)
        if data.get("follow"):
            other_user.followers.add(request.user.id)
        elif data.get("unfollow"):
            other_user.followers.remove(request.user.id)
        return JsonResponse({"followers_counter": other_user.followers.count(), "message": "you start follow this user"}, status=201)
    return JsonResponse({"message": "PUT request required"}, status=201)


@csrf_exempt
@login_required(redirect_field_name='index')
def following(request):
    posts_list = Post.objects.filter(user__followers__id=request.user.id).order_by("-created")
    paginator = Paginator(posts_list, 5) # Show 5 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "header": "All posts from users that I follow"
    })

@csrf_exempt
@login_required(redirect_field_name='index')
def edit_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        post.post = data["post"]
        post.save()
        return JsonResponse({"message": "Ok"}, status=201)
