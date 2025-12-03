from django.db import models
from django.conf import settings
from django.utils import timezone


class Ward(models.TextChoices): 
    
    MINATO    = "minato", "港区"
    CHIKUSA   = "chikusa", "千種区"
    ATSUTA    = "atsuta", "熱田区"
    NAKA      = "naka", "中区"
    KITA      = "kita", "北区"
    HIGASHI   = "higashi", "東区"
    NISHI     = "nishi", "西区"
    NAKAMURA  = "nakamura", "中村区"
    '''
    SHOWA     = "showa", "昭和区"
    MIZUHO    = "mizuho", "瑞穂区"
    NAKAGAWA  = "nakagawa", "中川区"
    MINAMI    = "minami", "南区"
    MORIYAMA  = "moriyama", "守山区"
    MEITO     = "meito", "名東区"
    TEMPAKU   = "tempaku", "天白区"
    MIDORI    = "midori", "緑区"
    '''
    
    
    
class Rating(models.IntegerChoices):
    ONE = 1, "★☆☆☆☆"
    TWO = 2, "★★☆☆☆"
    THREE = 3, "★★★☆☆"
    FOUR = 4, "★★★★☆"
    FIVE = 5, "★★★★★"
    
    
class Genre(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Spot(models.Model):
    name = models.CharField(max_length=50)
    ward = models.CharField(max_length=20, choices=Ward.choices)
    
    def __str__(self):
        return self.name
    
    
class SpotSubArea(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="subareas")
    name = models.CharField(max_length=30)
    ward = models.CharField(max_length=20, choices=Ward.choices)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["spot", "name", "ward"], name="unique_spot_subarea")
        ]
    
    def __str__(self):
        return f"{self.name}（{self.get_ward_display()}）"


class Restaurant(models.Model):  
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ward = models.CharField(max_length=20, choices=Ward.choices)
    sub_area = models.ForeignKey(SpotSubArea, on_delete=models.CASCADE, related_name="restaurant")
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to="restaurant_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.ManyToManyField(Genre)
    
    min_party_size = models.PositiveSmallIntegerField(default=1)
    max_party_size = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.name
    
    
class OpeningHour(models.Model):
    class Weekday(models.IntegerChoices):
        MON = 0, "月"
        TUE = 1, "火"
        WED = 2, "水"
        THU = 3, "木"
        FRI = 4, "金"
        SAT = 5, "土"
        SUN = 6, "日"
        
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="opening_hours")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "weekday", "open_time", "close_time"],
                name="unique_openinghour_slot")
        ]
        
    def __str__(self):
        return f"{self.get_weekday_display()} {self.open_time}〜{self.close_time}"
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=Rating.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.restaurant.name}'
    
    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    reserved_datetime = models.DateTimeField(null=True, blank=True)
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
    
    
class UserBilling(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="billing",)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True,)
    default_payment_method_id = models.CharField(max_length=255, blank=True, null=True,)
    card_brand = models.CharField(max_length=50, blank=True, null=True,)
    card_last4 = models.CharField(max_length=4, blank=True, null=True,)
    
    def __str__(self):
        return f"Billing info for {self.user}"