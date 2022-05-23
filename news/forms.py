from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea

from .models import RatingScore, Rating, News
from .utils import form_attributes, pagination_form_attributes


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'class': 'register_form'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginUserForm(AuthenticationForm):
    """Форма для аутентификации"""
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    score = forms.ModelChoiceField(label='Оценка', queryset=RatingScore.objects.all(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('score',)


class NewsForm(forms.ModelForm):
    """Форма для добавления новой статьи"""

    class Meta:
        model = News
        fields = ['title', 'short_description', 'description']
        widgets = {
            "title": Textarea(attrs={
                'class': 'form_news',
                'placeholder': 'Название статьи'}),
            'short_description': Textarea(attrs={
                'class': 'form_news',
                'placeholder': 'Краткое содержание статьи'}),
            'description': Textarea(attrs={
                'class': 'form_news',
                'placeholder': 'Полное содержание статьи'})}


class SearchForm(forms.Form):
    """Форма для сортировки"""
    new = forms.TypedMultipleChoiceField(label="Сортировать по:", choices=form_attributes,
                                         widget=forms.widgets.RadioSelect)


class PaginatorForm(forms.Form):
    """Форма для кол-ва новостей на странице"""
    pag = forms.TypedMultipleChoiceField(label="Кол-во новостей на странице:", choices=pagination_form_attributes,
                                         widget=forms.widgets.RadioSelect)
