from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from django import forms
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models.query import EmptyQuerySet

from .models import *

class CloseForm(forms.Form):
    closevar = forms.CharField(max_length=7,min_length=0)

class WatchForm(forms.Form):
    watchvar = forms.CharField(max_length=10,min_length=0)

class BidForm(forms.Form):
    price = forms.DecimalField(label="Place Your Bid ", max_digits=6, decimal_places=2)

class CommentForm(forms.Form):
    commentContent = forms.CharField()

class ListingForm(forms.Form):
    name = forms.CharField(max_length=150)
    
    categoryid = forms.CharField(max_length=10)
    imageurl = forms.CharField(max_length=600, required=False)
    price = forms.DecimalField(max_digits=6, decimal_places=2)

    description = forms.CharField(max_length=600)

def groupListings(listings):
    listingGroup = []
    listingGroupTotal = []
    listingCount = 0
    listingGroupCount = 0
    for listing in listings:
        listingGroup.append(listing)
        listingCount += 1
        if listingCount == 3:
            listingGroupTotal.append(listingGroup)
            listingGroup = []
            listingCount = 0
            listingGroupCount += 1
    listingGroupTotal.append(listingGroup)
    return listingGroupTotal

def index(request):
    groupedListings = groupListings(Listing.objects.all().filter(closed=False))

    return render(request, "auctions/index.html",{
        "listingGroupTotal": groupedListings,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request,id):
    error = False
    errorM = ""

    if request.user.is_authenticated:
        curUser = User.objects.get(username=request.user.username)
    curlisting = Listing.objects.get(pk=id)

    if curlisting is None:
        return render(request,"auctions/error.html",{
            "error": "Could not find listing"
        })

    if 'closevar' in request.POST:
        closeform = CloseForm(request.POST)
        if closeform.is_valid():
            closevar = closeform.cleaned_data["closevar"]
            if closevar == "Close":
                curlisting.closed = True
                curlisting.save()
        else:
            return render(request,"auctions/error.html",{
                "error": "Invalid Form"
            })

    if 'watchvar' in request.POST:
        watchform = WatchForm(request.POST)
        if watchform.is_valid():
            watchvar = watchform.cleaned_data["watchvar"]
            if watchvar == "Add":
                #add to watchlist
                curUser.watchlist.add(curlisting)
            else:
                #remove from the watchlist
                #check if remove() works
                curUser.watchlist.remove(curlisting)
        else:
            return render(request,"auctions/error.html",{
                "error": "Invalid Form"
            })

    if 'price' in request.POST:
        #create bid
        bidform = BidForm(request.POST)
        if bidform.is_valid():

            price = bidform.cleaned_data["price"]

            bidlist = curlisting.biddings.all()
            bidhighprice = 0
            if bidlist.exists():
                bidhighprice = bidlist.order_by('price').last().price

            if price < bidhighprice:
                error = True
                errorM = "You must bid higher than the highest bidding"
            else:
                created_date = models.DateTimeField(default=now, editable=False)
                bid = Bid.objects.create(author=curUser, price=price, time=created_date, listing=curlisting)
        
        else:
            return render(request,"auctions/error.html",{
                "error": "Invalid Form"
            })

    if 'commentContent' in request.POST:
        #create comment
        comm_form = CommentForm(request.POST)
        if comm_form.is_valid():
            content = comm_form.cleaned_data["commentContent"]

            created_date = models.DateTimeField(default=now, editable=False)
            comment = Comment.objects.create(author=curUser, content=content, time=created_date, listing=curlisting)
        else:
            return render(request,"auctions/error.html",{
                "error": "Invalid Form"
            })

    #Check for Watchlist
    try:
        watchcheck = curUser.watchlist.get(pk=id)
        watching = True
    except:
        watching = False


    #Load Biddings
    bidlist = curlisting.biddings.all()
    bidhighest = bidlist.order_by('price').last()
    if bidlist.exists():
        bidhighprice = bidlist.order_by('price').last().price
    else:
        bidhighprice = 0

    if curlisting.price > bidhighprice:
        curPrice = curlisting.price
    else:
        curPrice = bidhighprice

    #Load Comments
    comments = curlisting.comments.all()
        
    return render(request, "auctions/listing.html",{
                "listing": curlisting,
                "InWatch": watching,
                "biddings": bidlist,
                "bidhigh": bidhighest,
                "price": curPrice,
                "comments": comments,
                "IsAuthenticated": request.user.is_authenticated,
                "Iserror": error,
                "errorM" : errorM
            })

@login_required
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    currentUser = User.objects.get(username=request.user.username)

    groupedWatchList = groupListings(currentUser.watchlist.all())

    return render(request,"auctions/watchlist.html",{
        "watchingGroupTotal": groupedWatchList
    })

def category(request, cat_name):
    if cat_name == 0:
        groupedListings = groupListings(Listing.objects.all())
        return render(request,"auctions/category.html",{
            "listingGroupTotal": groupedListings,
            "categories": Category.objects.all()
        })
    curcat = Category.objects.get(id=cat_name)
    catList = curcat.listings.all()
    groupedListings = groupListings(catList)
    return render(request,"auctions/category.html",{
        "listingGroupTotal": groupedListings,
        "categories": Category.objects.all()
    })

def createListing(request):
    if request.user.is_authenticated:
        curUser = User.objects.get(username=request.user.username)
    else:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        listform = ListingForm(request.POST)
        print("POST received")
        print(listform.errors)
        if listform.is_valid():
            print("Form Valid")
            name = listform.cleaned_data["name"]
            imageurl = listform.cleaned_data["imageurl"]
            description = listform.cleaned_data["description"]
            price = listform.cleaned_data["price"]
            categoryid = listform.cleaned_data["categoryid"]
            category = Category.objects.get(id=categoryid)
            created_date = models.DateTimeField(default=now, editable=False)

            newlisting = Listing(name=name, author=curUser, category=category, imageurl=imageurl, price=price, description=description, time=created_date, closed=False)
            print(newlisting)
            newlisting.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/error.html",{
                "error": "Invalid Form"
            })
    return render(request,"auctions/createListing.html",{
        "category": Category.objects.all()
    })