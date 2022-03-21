from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Review, User, Movie


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["body", "rating"]


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {"password": forms.PasswordInput()}


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15)
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        field_classes = {"username": UsernameField}


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description", "rating", "release_year"]
