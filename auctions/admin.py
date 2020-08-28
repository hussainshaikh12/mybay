from django.contrib import admin

from .models import User, Auction_listing, Bids, Watch_list, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listing)
admin.site.register(Bids)
admin.site.register(Watch_list)
admin.site.register(Comments)