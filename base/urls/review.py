from django.urls import path
from base.views.review.review import RestaurantReviewCreateView, RestaurantReviewUpdateView, RestaurantReviewDeleteView

urlpatterns = [
    path("", RestaurantReviewCreateView.as_view(), name="restaurant_review_create"),
    path("<int:review_pk>/edit/", RestaurantReviewUpdateView.as_view(), name="restaurant_review_update"),
    path("<int:review_pk>/delete/", RestaurantReviewDeleteView.as_view(), name="restaurant_review_delete"),
]