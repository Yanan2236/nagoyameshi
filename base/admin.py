from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Restaurant, OpeningHour, Genre, Review, Reservation, Favorite, Subscription, Spot, SpotSubArea


class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [OpeningHourInline]
    filter_horizontal = ("genre",)
    
    search_fields = ("name", "address")
    list_filter = ("genre", "ward")
    

class SpotSubAreaInline(admin.TabularInline):
    model = SpotSubArea
    fields = ("name", "ward")
    extra = 1
    ordering = ("ward", "name")
    

class SpotAdmin(admin.ModelAdmin):
    inlines = [SpotSubAreaInline]
    
    
User = get_user_model()
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "username", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(Genre)
admin.site.register(Spot, SpotAdmin)
admin.site.register(SpotSubArea)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(User, BaseUserAdmin)
