from django import forms
from base.models import Ward, Genre


class SearchForm(forms.Form):
    ward = forms.ChoiceField(
        choices=Ward.choices,
        required=False,
        widget=forms.Select(attrs={"class": "search-select"})
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select"})
    )