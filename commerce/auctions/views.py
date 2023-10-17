from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms

from .models import User, Listing ,Comment, Bid ,Category

class BidForm(forms.Form):
    bid = forms.IntegerField()
    
class ListingForm(forms.Form):
    title = forms.CharField(max_length=64 , widget=forms.TextInput(attrs={'placeholder': 'Product name etc.', 'style': 'width: 300px;', }))
    description = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={ 'placeholder': 'Product details...', "style" : "widht : 300px;" , "rows":5 }))
    image = forms.ImageField()
    start_bid = forms.IntegerField(widget=forms.NumberInput(attrs = {'placeholder' : '$...', 'style':'width : 200px;'} ))
    
    #    Function to create category choices according to current categories
    def get_choices():
        category_choices = [ (category.id,category.category) for category in Category.objects.all()]
        return category_choices    

    category = forms.ChoiceField(choices=get_choices())

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=256)


def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all(),
        "is_empty" : Listing.objects.all().count() == 0
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


def categories(request):
    return render(request,"auctions/categories.html",{
        "categories" : Category.objects.all()
    })


"""
Function to view all of the listings specified by a category id 
! Here I used same page with active listing to not repeat my self 
"""
def category_view(request,category_id):
    category = Category.objects.get(id = category_id)
    return render(request, "auctions/index.html",{
        "listings" : category.listings.all(),
        "title" : category.category,
        "is_empty" : category.listings.all().count() == 0
    })


def create_listing(request) :

    if not request.user.is_authenticated:
        return render(request,"auctions/error_page.html") # or I might return you are not authenticated message here
    
    if request.method == "POST" :
        form = ListingForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            # get category from the form and assign it to Listing.category
            category_id = form.cleaned_data["category"]

            category_obj = Category.objects.get( id = category_id )

            listing_obj = Listing(title = form.cleaned_data["title"] , description = form.cleaned_data["description"], 
                                  image = form.cleaned_data["image"] , bottom_price = form.cleaned_data["start_bid"] ,
                                  bid_count = 0, owner = User.objects.get( username = request.user.username),category = category_obj
                                  )
            listing_obj.save()
            category_obj.save()

            return HttpResponseRedirect(reverse("index"))
        else :
            print("Listing form submitted wasn't valid")
            return HttpResponse("Form wasnt valid")
    else :

        return render(request,"auctions/create_listing.html",{
            "form" : ListingForm()
        })
    



"""
Function to view users watchlist
"""
def watch_list(request,username):
    # related_user = User.objects.get(username = username)
    related_user = request.user
    return render(request,"auctions/watch_list.html",{
        "user" : User.objects.get(username = username),
        "watch_list" : related_user.watch_list.all(),
        "is_empty" : related_user.watch_list.all().count() == 0,
    })

"""
Function to add a listing to users watchlist
"""
def add_to_watchlist(request, listing_id ):
    user = request.user
    l1 = Listing.objects.get(id = listing_id)
    user.watch_list.add(l1)
    
    return HttpResponseRedirect( reverse("listing",kwargs = {"listing_id" : listing_id}))


"""
Function to remove a listing to users watchlist
"""
def remove_from_watchlist(request, listing_id ):
    user = request.user
    l1 = Listing.objects.get(id = listing_id)
    user.watch_list.remove(l1)
    
    return HttpResponseRedirect( reverse("listing",kwargs = {"listing_id" : listing_id}))


"""
Function to add a comment to a listing
User info will be got from request
There will be only POST to this function 
CommentForm will be posted
"""
def add_comment(request,listing_id) : 
    form = CommentForm(request.POST)
    if form.is_valid() : 
        listing_obj = Listing.objects.get( id = listing_id )
        
        comment = form.cleaned_data["comment"]

        # create comment object
        comment_obj = Comment( related_listing = listing_obj, user = request.user, comment_text = comment )
        comment_obj.save()

        # return the rendered page with added comment

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}) )

    else:
        return HttpResponseRedirect("Invalid comment")


"""
Function to delete the comment that is added by the user
"""
def delete_comment(request,listing_id,comment_id):
    try:
        comment = Comment.objects.get( pk = comment_id)
    except Comment.DoesNotExist:   
        return HttpResponseRedirect("Comment Doesn't exist")

    user = comment.user
    listing = comment.related_listing

    comment.delete()

    user.save()
    listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs = {"listing_id" : listing_id}) )



'''
Function to display the specified listing with details.
'''
def listing(request,listing_id) : 
    print("Listing function")
    try :     
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist :
        listing = None
        return render(request, "auctions/error_page.html")
    
    user  = request.user
    in_users_watchlist = False
    # if listing element in users wathclis then in_users_watchlist == True
    # try to find the listing that is specified by listing_id in users watchlist
    if user.is_authenticated:
        print(user.watch_list.all())
        try :     
            listing_in_watchlist = user.watch_list.get(id=listing_id)
        except Listing.DoesNotExist :
            listing_in_watchlist = None

        if listing_in_watchlist != None : 
            in_users_watchlist = True
            
        print(f" {listing_in_watchlist} is {in_users_watchlist}")

    try : 
        current_bid = listing.bid.get()
    except Bid.DoesNotExist :
        current_bid = None

    return render(request,"auctions/listing.html",{
        "listing" : listing,
        "comments": listing.comments.all(),
        "bid_form" : BidForm(initial = { "bid": "0" } ),
        "current_bid" : current_bid,
        "user" : request.user,
        "comment_form" : CommentForm(),
        "in_users_watchlist": in_users_watchlist,
        "not_in_users_watchlist": bool(~in_users_watchlist),
        "date" : listing.date_string
    })




"""
Function to get the bid from form and update if needed
(optional) Otherwise bid is not accepted message can be sent
"""
def place_bid(request,listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id = listing_id)
        form = BidForm(request.POST)

        if form.is_valid() : 
            placed_bid = form.cleaned_data['bid']
            # if bid that is placed is not larger then current bid return a page with error message that indicates "Bids should be higher then current bid"
            if placed_bid <= listing.bottom_price :
                form.add_error('bid', f"Bid must be larger than {listing.bottom_price}.")
                '''
                The below code untill the else statement is the same code as listing function.
                Couldn't find better why to overcome this issue since min value is changing so :
                I couldn't use MinValidator etc.
                '''
                try :     
                    listing = Listing.objects.get(id=listing_id)
                except Listing.DoesNotExist :
                    listing = None
                    return render(request, "auctions/error_page.html")
                
                user  = request.user
                in_users_watchlist = False
                # if listing element in users wathclis then in_users_watchlist == True
                # try to find the listing that is specified by listing_id in users watchlist
                if user.is_authenticated:
                    print(user.watch_list.all())
                    try :     
                        listing_in_watchlist = user.watch_list.get(id=listing_id)
                    except Listing.DoesNotExist :
                        listing_in_watchlist = None

                    if listing_in_watchlist != None : 
                        in_users_watchlist = True
                        
                    print(f" {listing_in_watchlist} is {in_users_watchlist}")

                try : 
                    current_bid = listing.bid.get()
                except Bid.DoesNotExist :
                    current_bid = None

                return render(request,"auctions/listing.html",{
                    "listing" : listing,
                    "comments": listing.comments.all(),
                    "bid_form" : form,
                    "current_bid" : current_bid,
                    "user" : request.user,
                    "comment_form" : CommentForm(),
                    "in_users_watchlist": in_users_watchlist,
                    "not_in_users_watchlist": bool(~in_users_watchlist)
                })
            else :
                print("placed bid is larger")
                listing.bid_count += 1
                listing.bottom_price = placed_bid
                try : 
                    bid = listing.bid.get()
                except Bid.DoesNotExist :
                    bid = None
                if bid == None : 
                    bid = Bid(owner = request.user , value = placed_bid, related_listing = listing)
                else :
                    bid.owner = request.user
                    bid.value = placed_bid

                bid.save()
                listing.save()
                return HttpResponseRedirect(reverse("listing", kwargs = {"listing_id" : listing_id}))
            # return the page itself with updated bid
        else :
            print("Place Bid form is not valid")
            return render(request,"auctions/error_page.html")
    else : 
        return HttpResponseRedirect(reverse("listing",kwargs = {"listing_id" : listing_id}))



def close_auction(request,listing_id):
    listing = Listing.objects.get(id = listing_id)
    listing.active_listing = False
    listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}) )


"""
Function to display all of the listings and specific information about user
(Optional) If user page belongs to same person that is logged in then let user to edit the page 
"""
def user(request,username):
    pass