from django import forms
from base.models import Spot, Genre


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