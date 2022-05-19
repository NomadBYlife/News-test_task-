from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm, LoginUserForm
from .models import News, Author

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все авторы', 'url_name': 'all_author'}]


class NewsView(ListView):
    """Новости на страницу"""
    model = News
    template_name = 'news/main.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной сайт'
        context['menu'] = menu
        return context


class RegisterUserView(CreateView):
    """Регистрация"""
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация нового пользователя'
        context['menu'] = menu
        return context


class AllAuthorsView(ListView):
    """Список авторов"""
    model = Author
    template_name = 'news/authors_all.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все авторы'
        context['menu'] = menu
        return context


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все авторы'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')
