from django.urls import path
from .views.restaurant_views import (
    RestaurantListView,
    RestaurantDetailView,
)

app_name = "base"

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
]
