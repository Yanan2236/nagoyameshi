from django import forms
from base.models import Spot, Genre, Reservation


class SearchForm(forms.Form):
    spot = forms.ModelChoiceField(
        queryset=Spot.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select"})
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select"})
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