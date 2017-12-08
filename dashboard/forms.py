from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class SingleSearchForm(forms.Form):
    query_phrase = forms.CharField(max_length=200)




        # Remember to always return the cleaned data.
