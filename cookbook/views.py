import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import redirect

# Create your views here.
from .models import *

from django.core.paginator import Paginator, EmptyPage
from .forms import *

#UTIL
def groupRecipes(recipes):
    listingGroup = []
    recipeGroupTotal = []
    listingCount = 0
    listingGroupCount = 0
    for recipe in recipes:
        listingGroup.append(recipe)
        listingCount += 1
        if listingCount == 3:
            recipeGroupTotal.append(listingGroup)
            listingGroup = []
            listingCount = 0
            listingGroupCount += 1
    recipeGroupTotal.append(listingGroup)
    return recipeGroupTotal

def pagiRecipe(posts, perpage):
    #Use paginator to split post into groups
    postlist = []
    for post in posts:
        postlist.append(post)
    return Paginator(postlist, perpage)

def usernameInUserSet(input):
    #user_<namehere>
    name = input.slice(5)
    profileset = User.objects.values('username')
    for profile in profileset:
        print(profile['username'])
        if name == profile['username']:
            return True
    return False

#######################################################################################################

#VIEWS
def indexbase(request):
    return redirect('/index/1')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("indexbase"))
        else:
            return render(request, "cookbook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cookbook/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("indexbase"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cookbook/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cookbook/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("indexbase"))
    else:
        return render(request, "cookbook/register.html")

def profile(request, username, pagenum):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "cookbook/error.html")
    except Exception:
        return render(request, "cookbook/error.html")

    try:
        paginated = pagiRecipe(Recipe.objects.filter(author=user),9)
        recipepage = paginated.page(pagenum)
        recipeGroupTotal = groupRecipes(recipepage)
    except EmptyPage:
        recipeGroupTotal = None
        return render(request, "cookbook/profile.html", {
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'This page contains no results'
    })


    return render(request, "cookbook/profile.html", {
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'Success'
    })

def index(request,pagenum):
    try:
        paginated = pagiRecipe(Recipe.objects.all(),9)
        recipepage = paginated.page(pagenum)
        recipeGroupTotal = groupRecipes(recipepage)
    except EmptyPage:
        recipeGroupTotal = None
        return render(request, "cookbook/index.html", {
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'This page contains no results'
    })

    return render(request, "cookbook/index.html", {
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'Success'
    })

def search(request):
    pagenum = request.GET.get("pagenum", 1)
    
    if int(pagenum) is 1:
        isFirst = True
    else:
        isFirst = False

    keyword = request.GET.get("search", "")
    found = Recipe.objects.filter(title__contains=keyword)
    try:
        paginated = pagiRecipe(found,9)
        recipepage = paginated.page(pagenum)
        recipeGroupTotal = groupRecipes(recipepage)
    except EmptyPage:
        recipeGroupTotal = None
        return render(request, "cookbook/search.html", {
        'title': f'Searching for {keyword}',
        'keyword': keyword,
        'firstpage': isFirst,
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'This page contains no results'
        })
    return render(request, "cookbook/search.html", {
        'title': f'Searching for {keyword}',
        'keyword': keyword,
        'firstpage': isFirst,
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'Success'
    })

def liked(request):
    liked = Recipe.objects.filter(liked_by=request.user)
    pagenum = request.GET.get("pagenum", 1)
    if int(pagenum) is 1:
        isFirst = True
    else:
        isFirst = False
    try:
        paginated = pagiRecipe(liked,9)
        recipepage = paginated.page(pagenum)
        recipeGroupTotal = groupRecipes(recipepage)
    except EmptyPage:
        recipeGroupTotal = None
        return render(request, "cookbook/liked.html", {
        'firstpage': isFirst,
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'This page contains no results'
        })
    return render(request, "cookbook/liked.html", {
        'firstpage': isFirst,
        'currentpage': pagenum,
        'recipeGroupTotal': recipeGroupTotal,
        'message': 'Success'
    })

def recipePage(request,id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return render(request, "cookbook/error.html",{
            'message': 'Requested Recipe Does Not Exist'
        })
    return render(request, "cookbook/recipe.html",{
        'recipe': recipe
    })

@login_required(login_url='login')
def recipeEditPage(request,id):
    if request.method == "POST":
        print("POST request received")
        user = User.objects.get(username=request.user.username)
        editTarget = Recipe.objects.get(id=id)
        editTarget.title = request.POST['title']
        stepCount = int(request.POST['stepCount'])
        
        try:
            editTarget.image = request.FILES[f'mainImage']
        except Exception:
            print(f'mainImage not found, using existing image...')

        imgcopy = [editTarget.stepCount]
        for step in editTarget.steps.all():
            try:
                imgcopy[step.steporder] = step.image
            except Exception:
                pass

        editTarget.stepCount = stepCount
        editTarget.steps.all().delete()
        
        for i in range(stepCount):
            newStep = Step.objects.create()
            newStep.content = request.POST[f'step{i}']
            newStep.steporder = i
            newStep.recipe = editTarget
            try:
                newStep.image = request.FILES[f'img{i}']
            except Exception:
                print(f'img{i} not found, using existing image')
                try:
                    newStep.image = imgcopy[i]
                except Exception:
                    print(f'existing image for img{i} not found')
            newStep.save()

        editTarget.save()
        return HttpResponseRedirect(f'/recipe/{editTarget.id}')

    else:
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return render(request, "cookbook/error.html",{
                'message': 'Requested Recipe Does Not Exist'
            })
        if request.user.id == recipe.author.id:
            steps = recipe.steps.all()
            return render(request, "cookbook/editRecipe.html", {
                'recipe': recipe,
                'steps': steps
            })
        else:
            return render(request, "cookbook/error.html", {
                'message': 'User Not Allowed'
            })

@login_required(login_url='login')
def createRecipe(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(username=request.user.username)
        newRecipe = Recipe.objects.create(author=user)
        newRecipe.title = request.POST['title']
        stepCount = int(request.POST['stepCount'])
        newRecipe.stepCount = stepCount
        try:
            newRecipe.image = request.FILES[f'mainImage']
        except Exception:
            print(f'mainImage not found')

        for i in range(stepCount):
            newStep = Step.objects.create()
            newStep.content = request.POST[f'step{i}']
            newStep.steporder = i
            newStep.recipe = newRecipe
            try:
                newStep.image = request.FILES[f'img{i}']
            except Exception:
                print(f'img{i} not found')
            newStep.save()

        newRecipe.save()
        return HttpResponseRedirect(f'/recipe/{newRecipe.id}')
    else:
        return render(request, "cookbook/composeRecipe.html")

#######################################################################################################



# API Views
def getrecipe(request,recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        print(recipe)
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(recipe.serialize())

    elif request.method == "PUT":
        #like the recipe
        message = ""
        data = json.loads(request.body)
        print(recipe.liked_by.all())
        if data.get("like"):
            if request.user in recipe.liked_by.all():
                print(f"{request.user.username} unliked the post")
                recipe.liked_by.remove(request.user)
                message = "Unliked"
            else:
                print(f"{request.user.username} liked the post")
                recipe.liked_by.add(request.user)
                message = "Liked"

            recipe.save()
    else:
        return JsonResponse({"message": "Invalid Method"},status=404)
    return JsonResponse({"message": f"Successfully {message}"},status=200)