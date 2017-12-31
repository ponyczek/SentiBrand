from django import forms

from .models import User_Phrase


# for checking renewal date range.


class SingleSearchForm(forms.Form):
    query_phrase = forms.CharField(max_length=200)


class PhraseForm(forms.ModelForm):
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

    phrase = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Searched Phrase, person, tag'}),
        required=True)

    interval_in_sec = forms.IntegerField(
        initial=60,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder':'How frequently would you like to pull the data in seconds.'}),
        required=True
    )

    #
    class Meta:
        model = User_Phrase
        fields = ['name', 'start_date', 'interval_in_sec', 'phrase']
