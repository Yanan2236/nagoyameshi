from django.urls import path
from base.views.restaurant.list import RestaurantListView
from base.views.restaurant.detail import RestaurantDetailView
from base.views.restaurant.favorite import toggle_favorite
from base.views.review.review import RestaurantReviewCreateView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("<int:pk>/favorite/", toggle_favorite, name="toggle_favorite"),
    path("<int:pk>/reviews/new/", RestaurantReviewCreateView.as_view(), name="restaurant_review_create"),
]