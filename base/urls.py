from django.urls import path
from .views import (
    RestaurantListView,
    RestaurantDetailView,
)

app_name = "base"

urlpatterns = [
    path("restaurants/", RestaurantListView.as_view(), name="restaurant_list"),
    path("restaurants/<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
]
