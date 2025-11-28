from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from base.models import Reservation, Restaurant
from base.forms import ReservationForm
from base.mixins import SubscriptionRequiredMixin


class ReservationCreateView(SubscriptionRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "base/reservation/reservation_form.html"
    success_url = reverse_lazy("restaurant_reservation_list")
'''   ここ修正中！
    def form_valid(self, form):
        form.instance.user = self.request.user
        restaurant_id = self.request.GET.get("restaurant")
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        form.instance.restaurant = restaurant
        return super().form_valid(form)
'''

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "base/reservation/reservation_list.html"
    context_object_name = "reservations"
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-created_at")
    
    
class ReservationCancelView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = "base/reservation/reservation_cancel.html"
    success_url = reverse_lazy("reservation_list")
    context_object_name = "reservation"
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)