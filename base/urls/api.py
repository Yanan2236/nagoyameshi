from django.urls import path
from base.views.restaurant.list import RestaurantListView
from base.views.restaurant.detail import RestaurantDetailView
from base.views.api.restaurant_list import restaurant_list_api
from base.views.api.admin_restaurant_list import admin_restaurant_list

urlpatterns = [
    path("restaurants/", restaurant_list_api, name="api_restaurants"),
    path("owner/restaurants/", admin_restaurant_list, name="admin_restaurant_list"),
]