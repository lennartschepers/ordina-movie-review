from django import forms
from .models import Review
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'rating']

class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput()}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {'password': forms.PasswordInput(), 'email': forms.EmailInput(attrs={'required': True})}
