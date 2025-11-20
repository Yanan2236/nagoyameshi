from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField('Category', related_name='restaurants')

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.restaurant.name}'
    
    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    reserved_datetime = models.DateTimeField()
    number_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Reservation by {self.user.username} at {self.restaurant.name} on {self.reserved_datetime}'
    
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'restaurant'], name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user.username} favorited {self.restaurant.name}'
    
    
class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription',)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    @property
    def is_active(self) -> bool:
        return self.ended_at > timezone.now()