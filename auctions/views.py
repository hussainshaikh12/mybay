from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_listing, Bids, Watch_list, Comments
from .forms import CreateListing, listingComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from datetime import date

from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile


def index(request):
    Listings = Auction_listing.objects.all().filter(is_active=True)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if user:
            request.session['watchlist_count'] = Watch_list.objects.all().filter(user_id=user).count()
    return render(request, "auctions/index.html" , {
        "Listings" : Listings, 
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

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            upload_choice = form.cleaned_data["upload_choice"]
            user = User.objects.get(username=request.user.username)
            Listing = Auction_listing(user_id=user, name=title, price=price, description=description, category=category)
           
            if upload_choice == '1':
                files = request.FILES
                if files:
                    img = files["img"]
                    Listing.img = img
                    
            elif upload_choice == '2':
                img_url = form.cleaned_data["img_url"]
                if img_url:
                    name = urlparse(img_url).path.split('/')[-1]
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        Listing.img.save(name, ContentFile(response.content), save=True)

            Listing.save()

            messages.error(request, '✔️ Listing Created Successfully', extra_tags='success')
            # messages.error(request, files, extra_tags='success')
        # else:
        #     form = CreateListing()
    return render(request, "auctions/create_listing.html", {
        "form" : CreateListing()
    })

def listing(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    comments = Comments.objects.all().filter(al_id=Listing)
    maxBid = Bids.objects.all().filter(al_id=id).aggregate(Max('bid'))
    
    # messages.error(request, bidders_count, extra_tags='success')
    if maxBid['bid__max']:
        Listing.max_bid = maxBid['bid__max']
        Listing.save()
    
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        userBids_count = Bids.objects.all().filter(user_id=user, al_id=id).count()
        user_maxBid = Bids.objects.all().filter(user_id=user, al_id=id).aggregate(Max('bid'))
        all_Bids = Bids.objects.all().filter(al_id=id)
        in_WatchList = Watch_list.objects.all().filter(user_id=user, al_id=id)
        request.session['watchlist_count'] = Watch_list.objects.all().filter(user_id=user).count()

        return render(request, "auctions/listing.html" , {
        "Listing" : Listing, "user":user,
        "Comments":comments ,"in_WatchList":in_WatchList, 
        "commentForm":listingComment(), "all_Bids":all_Bids, "user_maxBid":user_maxBid['bid__max'],
        "userBids_count":userBids_count,
        })

    return render(request, "auctions/listing.html" , {
    "Listing" : Listing, "Comments":comments, "commentForm":listingComment(),
    })

@login_required(login_url="login")
def add_watch_list(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    in_WatchList = Watch_list.objects.all().filter(user_id=user, al_id=id)
    if in_WatchList:
        in_WatchList.delete()
        Listing.watchers_count -= 1
        Listing.save()
        return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))
    WatchList = Watch_list(user_id=user, al_id=Listing)
    WatchList.save()
    Listing.watchers_count += 1
    Listing.save()
    return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))

@login_required(login_url="login")
def watch_list(request):
    user = User.objects.get(username=request.user.username)
    WatchList = Watch_list.objects.all().filter(user_id=user)
    request.session['watchlist_count'] = Watch_list.objects.all().filter(user_id=user).count()
    return render(request, "auctions/watch_list.html", {
        "watch_list" : WatchList
    })

@login_required(login_url="login")      
def rem_watch_list(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    WatchList = Watch_list.objects.all().filter(user_id=user, al_id=id)
    WatchList.delete()
    Listing.watchers_count -= 1
    Listing.save()
    return HttpResponseRedirect(reverse("watch_list"))

@login_required(login_url="login")
def place_bid(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    in_Bids = Bids.objects.all().filter(user_id=user, al_id=id)
    if request.method == "POST":
        bid = request.POST["bid"]
        bids = Bids(user_id=user, al_id=Listing, bid=bid)
        bids.save()
        bidders_count = Bids.objects.filter(al_id=id).values('user_id').distinct().count()
        Listing.bids_count += 1
        Listing.bidders_count = bidders_count
        Listing.save()
        messages.error(request, "Bid placed successfully", extra_tags='success')
        return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))
    return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))
       
@login_required(login_url="login")
def add_comment(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    in_Comments = Comments.objects.all().filter(user_id=user, al_id=Listing)
    if request.method == "POST":
        if in_Comments:
            messages.error(request, "You have already placed a Comment", extra_tags='danger')
            return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))
        form = listingComment(request.POST)
        if form.is_valid():
            title = form.cleaned_data["comment_title"]
            comment = form.cleaned_data["comment"]
            listing_comment = Comments(user_id=user, al_id=Listing, comment_title=title, comment=comment)
            listing_comment.save()
            messages.error(request, "Comment Added", extra_tags='success')
            return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))
    return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))

def categories(request):
    Listings = Auction_listing.objects.all().filter(is_active=True)
    Categories = Auction_listing.objects.values('category').filter(is_active=True).distinct()
    if request.method == "GET":
        cat_selected = request.GET.get('category')
        if cat_selected != "all":
            Listings = Auction_listing.objects.all().filter(is_active=True, category=cat_selected)
            return render(request, "auctions/categories.html" , {"Listings" : Listings, "Categories":Categories, "cat_selected":cat_selected,})
        return render(request, "auctions/categories.html" , {
            "Listings" : Listings, "Categories":Categories,
            })


    return render(request, "auctions/categories.html" , {
    "Listings" : Listings, "Categories":Categories,
    })

def close_listing(request, id):
    Listing = Auction_listing.objects.get(pk=id)
    Listing.is_active = False
    Listing.sold_on = date.today()
    if Listing.max_bid:
        maxBidder = Bids.objects.all().filter(al_id=Listing, bid=Listing.max_bid).first()
        Listing.sold_to = maxBidder.user_id.username
    Listing.save()
    messages.error(request, "Listing Closed Successfully" , extra_tags='success')
    return HttpResponseRedirect(reverse("listing",kwargs={'id':id}))

@login_required(login_url="login")
def my_listings(request):
    user = User.objects.get(username=request.user.username)
    Listings = Auction_listing.objects.all().filter(user_id=user) 
    return render(request, "auctions/my_listings.html", {
        "Listings":Listings,
    })

@login_required(login_url="login")
def my_bids(request):
    Listings = Auction_listing.objects.all() 
    Listing_ids = Bids.objects.values('al_id').filter(user_id=request.user).distinct()
    return render(request, "auctions/my_bids.html", {
        "Listing_ids":Listing_ids, "Listings":Listings,
    })
