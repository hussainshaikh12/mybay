from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("add_watch_list/<str:id>",views.add_watch_list, name="add_watch_list"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("rem_watch_list/<str:id>", views.rem_watch_list, name="rem_watch_list"),
    path("place_bid/<str:id>", views.place_bid, name="place_bid"),
    path("add_comment/<str:id>", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("close_listing/<str:id>", views.close_listing, name="close_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_bids", views.my_bids, name="my_bids"),
]
