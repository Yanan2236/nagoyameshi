from django.contrib import admin
from .models import Restaurant, OpeningHour, Category, Review, Reservation, Favorite, Subscription


class OpeningHourInine(admin.TabularInline):
    model = OpeningHour
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [OpeningHourInine]
    list_filter = ("category",)
    filter_horizontal = ("category",)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(Favorite)
admin.site.register(Subscription)
