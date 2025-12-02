from django import forms
from base.models import Spot, Genre, Reservation, OpeningHour, Restaurant
from datetime import datetime, time
import json

class SearchForm(forms.Form):
    spot = forms.ModelChoiceField(
        queryset=Spot.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select search-field"})
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select search-field"})
    )
    restaurant_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "search-input search-field", "placeholder": "レストラン名"})
    )
    
    
'''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        restaurant = models.Restaurant.objects.filter(id=self.kwargs["pk"]).first()
        
        reservation_time = datetime.combine(date.today(),restaurant.open_time)
        close_time = datetime.combine(date.today(), restaurant.close_time)
        reservation_limit = close_time - timedelta(minutes=60)
        
        #予約時間選択候補生成
        time_choice = []

        while True:
            time_choice.append((reservation_time.time(), reservation_time.strftime("%H:%M")))
            reservation_time = reservation_time + timedelta(minutes=30)
            if reservation_time > reservation_limit:
                break

        kwargs["time_choice"] = time_choice
        
        #予約人数選択候補生成
        number_of_people_choice = []
        seats_number = restaurant.seats_number
        if seats_number > 50:
            seats_number =50
        
        for number in range(1, seats_number +1):
            number_of_people_choice.append((number, f"{number}名"))
        
        kwargs["number_of_people_choice"] = number_of_people_choice
        
        return kwargs

'''
        
class ReservationForm(forms.ModelForm):
    TIME_CHOICES = [
        (f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}")
        for h in range(0,23)
        for m in (0, 15, 30, 45)
    ]
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.ChoiceField(choices=TIME_CHOICES, required=True,)
    number_of_people = forms.TypedChoiceField(choices=(), coerce=int, required=True)
     
    class Meta:
        model = Reservation
        fields = ["number_of_people"]
        
    def __init__(self, *args, restaurant=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurant = restaurant
        self.user = user
        
        if self.restaurant is None:
            raise ValueError("ReservationForm requires a restaurant instance")
        
        min_size = self.restaurant.min_party_size
        max_size = self.restaurant.max_party_size
            
        party_range = range(min_size, max_size + 1)
        party_choices = [(p, f"{p}人") for p in party_range]
        self.fields["number_of_people"].choices = party_choices

        open_dates = set(self.restaurant.opening_hours.values_list("weekday", flat=True))
        alldates = set(OpeningHour.Weekday.values)
        self.closed_dates = alldates - open_dates
        # 休業日情報をdateフィールドに付与し、JSでカレンダーに休業日を反映する。
        self.fields["date"].widget.attrs["data-closed-weekdays"] = json.dumps(sorted(self.closed_dates, key=OpeningHour.Weekday.values.index))
        
    def clean_time(self):
        raw = self.cleaned_data.get("time")
        hour_str, minute_str = raw.split(":")
        return time(hour_str, minute_str)
    
            
    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")
        
        if d and t:
            weekday = d.weekday()
            is_open = OpeningHour.objects.filter(
                restaurant=self.restaurant,
                start_time__lte=t,
                end_time__lte=t,
            ).exists() 
            if not is_open:
                self.add_error("time", "この日時は営業時間外です。")
                return cleaned
            
            cleaned["resreved_datetime"] = datetime.combine(d, t)
        return cleaned
            
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.reserved_datetime = self.cleaned_data["reserved_datetime"]
        if commit:
            obj.save()
        return obj