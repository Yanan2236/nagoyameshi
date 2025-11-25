from django.views.generic import DetailView
from base.models import Restaurant, Favorite, Review
    
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
            
        context["genres"] = restaurant.genre.all()
        context["reviews"] = restaurant.reviews.select_related("user").all()

        return context