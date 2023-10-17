from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_view, name="categories"),
    path("create_listing",views.create_listing,name="create_listing"),
    path("listing/<int:listing_id>",views.listing, name="listing"),
    path("watch_list/<str:username>",views.watch_list,name="watch_list"),
    path("add_to_watchlist/<int:listing_id>",views.add_to_watchlist,name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>",views.remove_from_watchlist,name="remove_from_watchlist"),
    path("add_comment/<int:listing_id>",views.add_comment,name = "add_comment"),
    path("delete_comment/<int:listing_id>/<int:comment_id>",views.delete_comment,name = "delete_comment"),
    path("place_bid/<int:listing_id>",views.place_bid,name="place_bid"),
    path("user/<str:username>",views.user,name="user"),    
    path("close_auction/<int:listing_id>",views.close_auction,name = "close_auction")

]
