from django.urls import path
from base.views.restaurant.list import RestaurantListView
from base.views.restaurant.detail import RestaurantDetailView
from base.views.api.restaurant_list import restaurant_list_api

urlpatterns = [
    path("restaurants/", restaurant_list_api, name="api_restaurants")
]