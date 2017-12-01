#log/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', type:'password', 'name': 'password'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', type:'password', 'name': 'password'}))

    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
