from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=10)
    max_bid = models.FloatField(max_length=10, blank=True , null=True)
    watchers_count = models.IntegerField(blank=True, default=0)
    bidders_count = models.IntegerField(blank=True, default=0)
    bids_count = models.IntegerField(blank=True, default=0)
    description = models.TextField(blank=True , null=True)
    category = models.CharField(max_length=20, blank=True)
    img = models.ImageField(blank=True, null=True, default="default_img.png")
    created_on  = models.DateField(auto_now_add=True)
    sold_on  = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sold_to = models.CharField(max_length=150, blank=True, null=True)
    # sold_for = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Product:{self.name} listed by {self.user_id}"

class Bids(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, )
    al_id  = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, )
    bid = models.FloatField(max_length=10)
    created_on  = models.DateField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.user_id} bid {self.bid} on {self.al_id}"

class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, )
    al_id  = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, )
    comment_title = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=250)
    created_on = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user_id} commented {self.comment_title} on {self.al_id}"

class Watch_list(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    al_id  = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing")
    def __str__(self):
        return f"Product:{self.al_id} added to watchlist by {self.user_id}"
