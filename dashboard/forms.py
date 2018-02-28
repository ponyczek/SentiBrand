from django import forms

from .models import User_Phrase


# for checking renewal date range.


class SingleSearchForm(forms.Form):
    query_phrase = forms.CharField(max_length=200)


class PhraseForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Name of your phrase, helps to organise your phrases'}))

    start_date = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime-local',
                'class': 'form-control',
                 'placeholder': 'Tracking start date'}),
        input_formats=['%Y-%m-%dT%H:%M'])

    end_date = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime-local',
                'class': 'form-control',
                 'placeholder': 'Tracking end date'}),
        input_formats=['%Y-%m-%dT%H:%M'])

    phrase = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Searched Phrase, person, tag'}),
        required=True)


    #
    class Meta:
        model = User_Phrase
        fields = ['name', 'start_date', 'end_date', 'phrase']
