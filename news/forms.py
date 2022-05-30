from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea

from .models import RatingScore, Rating, News
from .utils import form_attributes


class RegisterUserForm(UserCreationForm):
    """Register form"""
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'class': 'register_form'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginUserForm(AuthenticationForm):
    """Form for authentication"""
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))


class RatingForm(forms.ModelForm):
    """Form for adding a rating"""
    score = forms.ModelChoiceField(label='Score', queryset=RatingScore.objects.all(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('score',)


class NewsForm(forms.ModelForm):
    """Form for adding new article"""

    class Meta:
        model = News
        fields = ['title', 'short_description', 'description']
        widgets = {
            "title": Textarea(attrs={
                'class': 'form_news'}),
            'short_description': Textarea(attrs={
                'class': 'form_news'}),
            'description': Textarea(attrs={
                'class': 'form_news'}),
        }


class SortForm(forms.Form):
    """Form for sort"""
    new = forms.TypedMultipleChoiceField(label="Sort: ", choices=form_attributes,
                                         widget=forms.widgets.RadioSelect)
