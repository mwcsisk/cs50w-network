import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .functions import get_posts, get_page_number


# Page views

def index(request):
    posts = get_posts(request)
    page_no = get_page_number(request)

    return render(request, "network/index.html", {
        "posts": posts.page(page_no)
    })


@login_required
def following(request):
    if not request.user.following.all():
        return render(request, "network/not_following.html")
    posts = get_posts(request, users=request.user.following.all().values('id'))
    page_no = get_page_number(request)

    return render(request, "network/following.html", {
        "posts": posts.page(page_no)
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


def profile(request, username):
    # Render a given user profile
    user = User.objects.get(username=username)
    if request.user.is_authenticated:
        is_following = request.user.following.filter(id=user.id).exists()
    else:
        is_following = False
    
    posts = get_posts(request, username=username)
    page_no = get_page_number(request)

    return render(request, "network/profile.html", {
        "username": username,
        "following": user.following.count(),
        "followers": user.followers.count(),
        "posts": posts.page(page_no),
        "is_following": is_following
    })


# API views

@csrf_exempt
@login_required
def post(request):
    # API for new posts so we can post without user leaving the page

    # Make sure we got this as a POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Also make sure the user is actually logged in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in."}, status=400)
    
    # Make sure the post isn't empty or above character count
    data = json.loads(request.body)
    if len(data["body"]) <= 0:
        return JsonResponse({"error": "The body of the new post is empty."}, status=400)
    elif len(data["body"]) > 250:
        return JsonResponse({"error": "Post exceeds 250 characters."}, status=400)
    
    # Process post
    post = Post(author=request.user, body=data["body"])
    post.save()

    # Return the newly-created post so it can be added to the view
    return JsonResponse(post.serialize())

@csrf_exempt
@login_required
def follow(request):
    # API for follow/unfollow action

    # Confirm PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    # Confirm there's a logged-in user
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in."}, status=400)
    
    # Get the body of the request
    data = json.loads(request.body)
    followee = User.objects.get(username=data["followee"])

    if not followee:
        return JsonResponse({"error": "User {} does not exist in the database".format(data["followee"])}, status=400)
    
    # Process the follow toggle
    # We don't need to check if the follow already exists since .add() handles that for us
    if data["action"] == "follow":
        request.user.following.add(followee)
    elif data["action"] == "unfollow":
        request.user.following.remove(followee)
    else:
        return JsonResponse({"error": "Action must be either 'follow' or 'unfollow'"}, status=400)
    
    # Save our changes and return a 204 response
    request.user.save()
    return HttpResponse(status=204)


@csrf_exempt
@login_required
def edit(request):
    # API for editing a post

    # Check method and that user is logged in
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must be logged in."}, status=400)
    
    # Get the post we're editing
    data = json.loads(request.body)
    post = Post.posts.get(id=data["post"])

    # Make sure the user is actually the post's author
    if request.user != post.author:
        return JsonResponse({"error": "You can't edit someone else's post!"}, status=400)

    # Update post and send it back to the client
    post.body = data["body"]
    post.save()

    return JsonResponse({"body": post.body})


@csrf_exempt
@login_required
def like(request):
    # API for liking a post

    # Check method and that user is logged in
    if request.method != "PUT":
        return JsonResponse({"error": "PUT method required"},status=400)
    
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must be logged in."},status=400)
    
    data = json.loads(request.body)
    post = Post.posts.get(pk=data["post"])

    if data["action"] == "like":
        post.likes.add(request.user)
    elif data["action"] == "unlike":
        post.likes.remove(request.user)
    else:
        return JsonResponse({"error": "Invalid action."},status=400)
    
    post.save()

    return JsonResponse({"likes": post.likes.count()})