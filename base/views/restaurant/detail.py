from django.views.generic import DetailView
from base.models import Restaurant

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "base/restaurant/detail.html"