# log/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', type: 'password', 'name': 'password'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', type: 'password', 'name': 'password'}))

    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

#
class EditProfileForm(forms.ModelForm):
    # template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class EditProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'avatar',
        )


    # def clean_password(self):

    # copy functionality provided by UserChangeForm
