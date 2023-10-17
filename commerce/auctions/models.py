from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime  
from django.utils import timezone

def current_date():
    return datetime.now()

def current_time():
    return timezone.now().time()

def date_string(): 
    date = current_date()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    month = months[date.month - 1]
    return f"{month}. {date.day}, {date.year}, {date.hour}:{date.minute}"


class User(AbstractUser):
    username = models.CharField(primary_key=True, max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class Category(models.Model):
    id = models.BigAutoField(primary_key = True)
    category = models.CharField(max_length=64)
    @classmethod
    def get_default_category(mdl):
        ctgr, created = mdl.objects.get_or_create(
            id = 1 , 
            defaults=dict(category='Default Category'),
        )
        return ctgr.pk
        

"""
Configurations of the model will be changed if needed (probably).
It is just draft now.
"""
class Listing(models.Model) :
    id = models.BigAutoField(primary_key=True)    
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    image = models.ImageField(upload_to = "images/", default = "images/default.jpg")
    bottom_price = models.IntegerField(default = 0)
    bid_count = models.IntegerField(default = 0)
    # Here listings is a reverse name such that I can acces the listings of an owner by     "owner1.object.listings.all()" 
    owner = models.ForeignKey( User , on_delete=models.CASCADE ,related_name = "listings" )
    watch_listed = models.ManyToManyField( User , related_name = "watch_list", default = None )
    date = models.DateTimeField(default = current_date)
    date_string = models.CharField(max_length = 64, default = date_string)
    category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, default = Category.get_default_category, related_name="listings")
    is_active_listing = models.BooleanField(default = True)
    
    @classmethod
    def get_default_listing(mdl):
        ctgr, created = mdl.objects.get_or_create(
            id = 1 , 
            defaults=dict(title='Default Listing', description = "Default Description"),
        )
        return ctgr.pk        

class Comment(models.Model):
    id = models.BigAutoField(primary_key = True)
    related_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments",default = None) # Listing that comments that made
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="comments",default=None)        # User that typed the comment
    comment_text = models.CharField(max_length = 256,default="DEFAULT COMMENT")                                               # Comments itself


class Bid(models.Model):
    id = models.BigAutoField(primary_key = True)
    value = models.IntegerField()
    # A listing can only have one current bid 
    # So related name will be bid which indicates singularity  
    # When a new bid taken current bid object will be deleted and new one will be assigned 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bids",default=None) 
    related_listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bid", default=None)