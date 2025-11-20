from django.views.generic import ListView
from base.models import Restaurant

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"
    paginate_by = 10