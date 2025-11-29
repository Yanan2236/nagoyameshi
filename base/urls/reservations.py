from django.urls import path
from base.views.reservations.reservations import ReservationListView, ReservationCreateView, ReservationCancelView

urlpatterns = [
    path("", ReservationListView.as_view(), name="restaurant_reservation_list"),
    path("new/<int:restaurant_pk>/", ReservationCreateView.as_view(), name="restaurant_reservation_create"),
    path("<int:pk>/cancel/", ReservationCancelView.as_view(), name="restaurant_reservation_cancel"),
]