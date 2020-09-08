import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .models import *
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt, csrf_protect

#UTIL
def pagiPost(posts, perpage):
    #Use paginator to split post into groups
    postlist = []
    for post in posts:
        postlist.append(post)
    return Paginator(postlist, perpage)

def usernameInUserSet(name):
    profileset = User.objects.values('username')
    for profile in profileset:
        print(profile['username'])
        if name == profile['username']:
            return True
    return False


#Path
def index(request):
    return render(request, "network/index.html")


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

def profile(request, name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return render(request, "network/error.html")
    return render(request, "network/profilepage.html", {
        "pageuser": user
    })

@login_required(login_url='login')
def following(request):
    return render(request, "network/following.html")


#API routes
def newpost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        author  = request.user
        content = data.get("content")
        newpost = Post(
            author = author,
            content = content,
        )
        newpost.save()

        return JsonResponse({"message": "Post created successfully."}, status=201)

    else:
        return JsonResponse({"error": "Method not POST"}, status=404)

@csrf_exempt
def post(request, post_id):
    def editPost(post, data):
        if(post.author == request.user):
            post.content = data.get("content")
        else:
            raise ValueError("User not authorized")

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
        print(post)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post on PUT request
    elif request.method == "PUT":
        if request.user.is_authenticated:
            message = ""
            data = json.loads(request.body)
            print(post.liked_by.all())
            if data.get("like"):
                if request.user in post.liked_by.all():
                    print(f"{request.user.username} unliked the post")
                    post.liked_by.remove(request.user)
                    message = "Unliked"
                else:
                    print(f"{request.user.username} liked the post")
                    post.liked_by.add(request.user)
                    message = "Liked"
                    
            elif data.get("content") != None:
                try:
                    editPost(post, data)
                    message = "Edited"
                except ValueError as error:
                    return JsonResponse({"message": "User not authenticated"}, status=401)
            else:
                return JsonResponse({"error": "Invalid PUT Command"}, status=401)
        else:
            return JsonResponse({"message": "User not authenticated"}, status=401)
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
    post.save()
    return JsonResponse({"message": f"Successfully {message}"},status=200)

@csrf_exempt
def posts(request, batchtype, pagenum):
    #returns list of posts for the certain pagenum
    if batchtype == "all":
        #return all posts
        posts = Post.objects.all()
        
    elif batchtype == "following":
        #return only the posts by following users
        followUsers = User.objects.filter(followers=request.user)
        posts = Post.objects.filter(author__in=followUsers)

    elif usernameInUserSet(batchtype):
        #return all posts by the specified user
        pageuser = User.objects.get(username=batchtype)
        posts = Post.objects.filter(author=pageuser.id)

    else:
        return JsonResponse({"error": "Invalid Batchtype"}, status=400)

    posts = posts.order_by("-timestamp").all()
    paginated = pagiPost(posts, 10)
    try:
        org_posts = paginated.page(pagenum)
        print(org_posts)
        for post in org_posts:
            print(post)
        return JsonResponse([post.serialize() for post in org_posts], safe=False)
    except EmptyPage:
        return JsonResponse({"error": "No page for the given page number"}, status=400)

def follow(request, pageusername):
    if request.method == "PUT" and request.user.is_authenticated:
        data = json.loads(request.body)
        pageuser = User.objects.get(username=pageusername)
        if data.get("follow"):
            if request.user in pageuser.followers.all():
                print(f"{request.user.username} unliked the post")
                pageuser.followers.remove(request.user)
                message = "Unfollowed"
            else:
                print(f"{request.user.username} liked the post")
                pageuser.followers.add(request.user)
                message = "Followed"

            pageuser.save()
            return JsonResponse({"message": f"Successfully {message}"},status=200)
        else:
            return JsonResponse({'error': 'Undefined action'}, status=400)
    
    if request.method == "GET" and request.user.is_authenticated:
        pageuser = User.objects.get(username=pageusername)
        return JsonResponse({'following': request.user in pageuser.followers.all()}, status=200)
    
    else:
        return JsonResponse({'error': 'Incorrect request method'}, status=400)
