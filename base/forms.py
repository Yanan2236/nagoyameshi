from django import forms
from base.models import Spot, Genre, Reservation


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
    class Meta:
        model = Reservation
        fields = ["date", "time", "number_of_people"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "number_of_people": forms.NumberInput(attrs={"min": 1})
        }