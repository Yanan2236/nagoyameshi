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
        
        self.min_size = self.restaurant.min_party_size
        self.max_size = self.restaurant.max_party_size
            
        party_range = range(self.min_size, self.max_size + 1)
        party_choices = [(p, f"{p}人") for p in party_range]
        self.fields["number_of_people"].choices = party_choices

        open_dates = set(
            int(w) for w in self.restaurant.opening_hours.values_list("weekday", flat=True)
        )
        alldates = {choice.value for choice in OpeningHour.Weekday}
        self.closed_dates = sorted(alldates - open_dates)

        self.fields["date"].widget.attrs["data-closed-weekdays"] = json.dumps(self.closed_dates)
        # 休業日情報をdateフィールドに付与し、JSでカレンダーに休業日を反映する。
        self.fields["date"].widget.attrs["data-closed-weekdays"] = json.dumps(self.closed_dates)
        
    def clean_time(self):
        # tryしたほうがいいかも。
        raw = self.cleaned_data.get("time")
        hour, minute = map(int, raw.split(":"))
        return time(hour, minute)
    
    def clean_number_of_people(self):
        n = self.cleaned_data.get("number_of_people")
        
        if n is None:
            raise forms.ValidationError("人数を入力してください")
        
        if not (self.min_size <= n <= self.max_size):
            raise forms.ValidationError("人数が規定範囲外です")
        
        return n  
        
    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")
        
        if d and t:
            weekday = d.weekday()
            is_open = OpeningHour.objects.filter(
                restaurant=self.restaurant,
                weekday=weekday,
                open_time__lte=t,
                close_time__gte=t,
            ).exists()
            if not is_open:
                self.add_error("time", "営業時間外です。")
                return cleaned
            
            cleaned["resereved_datetime"] = datetime.combine(d, t)
        return cleaned
            
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.reserved_datetime = self.cleaned_data["resereved_datetime"]
        if commit:
            obj.save()
        return obj