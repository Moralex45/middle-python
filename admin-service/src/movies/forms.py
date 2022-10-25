from dal import autocomplete
from .models import PersonFilmWork
from django import forms


class PersonFilmWorkForm(forms.ModelForm):
    class Meta:
        model = PersonFilmWork
        fields = ('__all__')
        widgets = {
            'person': autocomplete.ModelSelect2()
        }
