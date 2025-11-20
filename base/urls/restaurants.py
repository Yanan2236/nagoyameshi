from django.urls import path
from base.views.restaurant.list import RestaurantListView
from base.views.restaurant.detail import RestaurantDetailView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
]