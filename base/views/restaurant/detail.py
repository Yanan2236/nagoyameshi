from django.views.generic import DetailView
from base.models import Restaurant, Favorite, Review, Reservation, OpeningHour
    
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "base/restaurant/detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        user = self.request.user

        if user.is_authenticated:
            context["is_favorited"] = Favorite.objects.filter(
                user=user,
                restaurant=restaurant
            ).exists()
        else:
            context["is_favorited"] = False
            
        if user.is_authenticated:
            context["user_review"] = Review.objects.filter(
                user=user,
                restaurant=restaurant
            ).first()
        else:
            context["user_review"] = None
            
        if user.is_authenticated:
            context["user_reservation"] = Reservation.objects.filter(
                user=user,
                restaurant=restaurant
            ).exists()
        else:
            context["user_reservation"] = None
            
        hours = (restaurant.opening_hours.all().order_by("weekday", "open_time"))
        weekday_to_slots = {}
        for h in hours: 
            weekday_to_slots.setdefault(h.weekday, []).append((h.open_time.strftime("%H:%M"), h.close_time.strftime("%H:%M")))
        grouped = {}
        for weekday, slots in weekday_to_slots.items():
            key = tuple(slots)
            grouped.setdefault(key, []).append(weekday)
        display_groups = []
        for slots, days in grouped.items():
            day_labels = [OpeningHour.Weekday(day).label for day in days]
            display_groups.append({
                "days": day_labels,
                "slots": slots,
            })
        all_days = {choice.value for choice in OpeningHour.Weekday}
        closed_days = sorted(all_days - set(weekday_to_slots.keys()))
        if not closed_days:
            closed_display = "定休日無し"
        else:
            closed_display = "・".join(
                OpeningHour.Weekday(day).label for day in closed_days
            )
        context["opening_groups"] = display_groups
        context["closed_display"] = closed_display
        
            
        context["genres"] = restaurant.genre.all()
        context["reviews"] = restaurant.reviews.select_related("user").all()

        return context