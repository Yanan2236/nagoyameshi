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
    
    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["restaurant"] = self.restaurant
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = self.restaurant
        return super().form_valid(form)
    

    
    '''
        def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        restaurant = models.Restaurant.objects.filter(id=self.kwargs["pk"]).first()
        
        reservation_time = datetime.combine(date.today(),restaurant.open_time)
        close_time = datetime.combine(date.today(), restaurant.close_time)
        reservation_limit = close_time - timedelta(minutes=60)
        
        #予約時間選択候補生成
        time_choice = []

        while True:
            time_choice.append((reservation_time.time(), reservation_time.strftime("%H:%M")))
            reservation_time = reservation_time + timedelta(minutes=30)
            if reservation_time > reservation_limit:
                break

        kwargs["time_choice"] = time_choice
        
        #予約人数選択候補生成
        number_of_people_choice = []
        seats_number = restaurant.seats_number
        if seats_number > 50:
            seats_number =50
        
        for number in range(1, seats_number +1):
            number_of_people_choice.append((number, f"{number}名"))
        
        kwargs["number_of_people_choice"] = number_of_people_choice
        
        return kwargs

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
    success_url = reverse_lazy("restaurant_reservation_list")
    context_object_name = "reservation"
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)