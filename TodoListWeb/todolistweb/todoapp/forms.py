from django import forms
from .models import CustomUser, User
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')