from django.db import models
from django.conf import settings
from django.utils import timezone


class Weekday(models.TextChoices):
    MON = "mon", "Mon"
    TUE = "tue", "Tue"
    WED = "wed", "Wed"
    THU = "thu", "Thu"
    FRI = "fri", "Fri"
    SAT = "sat", "Sat"
    SUN = "sun", "Sun"
    

class Ward(models.TextChoices):
    CHIKUSA   = "chikusa", "千種区"
    HIGASHI   = "higashi", "東区"
    KITA      = "kita", "北区"
    NISHI     = "nishi", "西区"
    NAKAMURA  = "nakamura", "中村区"
    NAKA      = "naka", "中区"
    SHOWA     = "showa", "昭和区"
    MIZUHO    = "mizuho", "瑞穂区"
    ATSUTA    = "atsuta", "熱田区"
    NAKAGAWA  = "nakagawa", "中川区"
    MINATO    = "minato", "港区"
    MINAMI    = "minami", "南区"
    MORIYAMA  = "moriyama", "守山区"
    MEITO     = "meito", "名東区"
    TEMPAKU   = "tempaku", "天白区"
    MIDORI    = "midori", "緑区"
    
    
class Genre(models.TextChoices):
    OGURA_TOAST      = "ogura_toast", "小倉トースト"
    DOTE_NI          = "dote_ni", "どて煮"
    TEBASAKI         = "tebasaki", "手羽先"
    TENMUSU          = "tenmusu", "天むす"
    TAIWAN_RAMEN     = "taiwan_ramen", "台湾ラーメン"
    ANKAKE_SPAGHETTI = "ankake_spaghetti", "あんかけスパゲッティ"
    KISHIMEN         = "kishimen", "きしめん"
    MISO_NIKOMI      = "miso_nikomi_udon", "味噌煮込みうどん"
    MISO_KATSU       = "miso_katsu", "味噌カツ"
    HITSUMABUSHI     = "hitsumabushi", "ひつまぶし"
    
    
class Rating(models.IntegerChoices):
    ONE = 1, "★☆☆☆☆"
    TWO = 2, "★★☆☆☆"
    THREE = 3, "★★★☆☆"
    FOUR = 4, "★★★★☆"
    FIVE = 5, "★★★★★"
    

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ward = models.CharField(max_length=20, choices=Ward.choices)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=30, choices=Genre.choices)

    def __str__(self):
        return self.name
    
    
class OpeningHour(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="opening_hours")
    weekday = models.IntegerField(choices=Weekday.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    
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