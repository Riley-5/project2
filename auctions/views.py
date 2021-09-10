from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import * 
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Max


def index(request):
    active_listings = []

    for item in Listing.objects.all():
        if item.active is True:
            active_listings.append(item)

    return render(request, "auctions/index.html", {
        "listings": active_listings
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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            item = form.save(commit = False)
            item.owner = request.user
            item.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing(request, listing_id):
    item = Listing.objects.get(pk = listing_id)
    top_3 = Bid.objects.filter(listing__pk = listing_id).order_by('-bid')[:3]
    top_bid = Bid.objects.filter(listing__pk = listing_id).aggregate(Max('bid'))['bid__max']
    winner = Bid.objects.filter(listing__pk = listing_id).order_by('-bid')[:1]  
    if top_bid == None:
        top_bid = 0

    #comments
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.owner = request.user
            new_comment.listing_id = listing_id
            new_comment.save()
            return render(request, "auctions/listing.html", {
                "item": item,
                "commment_form": CommentForm(),
                "bid_form": BidForm(),
                "top_3": top_3
            })
    else:
        comment_form = CommentForm()

    #bids
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid = bid_form.cleaned_data["bid"]
            if bid >= item.starting_price:
                if bid > top_bid:
                    new_bid = bid_form.save(commit = False)
                    new_bid.owner = request.user
                    new_bid.listing_id = listing_id
                    new_bid.save()
                    return render(request, "auctions/listing.html", {
                        "item": item,
                        "comment_form": CommentForm(),
                        "bid_form": BidForm(),
                        "top_3": top_3
                    })
            else:
                error_message = "ERROR: Bid has be to be greater than or equal to the starting price and greater than any other bids."
                return render(request, "auctions/listing.html", {
                        "item": item,
                        "comment_form": CommentForm(),
                        "bid_form": BidForm(),
                        "top_3": top_3,
                        "error_message": error_message
                })
    else:
        bid_form = BidForm()

    #close auction
    if request.method == "POST":
        item.active = False
        item.save()

        return render(request, "auctions/listing.html", {
        "item": item,
        "comment_form": CommentForm(), 
        "bid_form": BidForm(),
        "winners": winner
        })
        
    return render(request, "auctions/listing.html", {
        "item": item,
        "comment_form": CommentForm(),
        "bid_form": BidForm(),
        "top_3": top_3,
        "winners": winner 
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.CATEGORIES
    })

def category_items(request, category):
    category = Listing.objects.filter(category = category)
    return render(request, "auctions/category_items.html", {
        "category": category
    })

def add_watchlist(request, listing_id):
    item_for_watchlist = Listing.objects.get(pk = listing_id)
    if Watchlist.objects.filter(user = request.user, listing = listing_id).exists():
        return HttpResponseRedirect(reverse('index'))
    user_watchlist, created = Watchlist.objects.get_or_create(user = request.user)
    user_watchlist.listing.add(item_for_watchlist)
    item_for_watchlist.on_watchlist = True
    item_for_watchlist.save()
    watchlist = Watchlist.objects.get(user = request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def watchlist(request):
    watchlist = Watchlist.objects.get(user = request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })