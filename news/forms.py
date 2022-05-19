from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'class': 'register_form'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')