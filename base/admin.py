from django.contrib import admin
from .models import Restaurant, OpeningHour, Genre, Review, Reservation, Favorite, Subscription, Spot, SpotSubArea


class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [OpeningHourInline]
    filter_horizontal = ("genre",)
    

class SpotSubAreaInline(admin.TabularInline):
    model = SpotSubArea
    extra = 1
    

class SpotAdmin(admin.ModelAdmin):
    inlines = [SpotSubAreaInline]


admin.site.register(Genre)
admin.site.register(Spot, SpotAdmin)
admin.site.register(SpotSubArea)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(Favorite)
admin.site.register(Subscription)
