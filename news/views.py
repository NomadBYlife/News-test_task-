from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm
from .models import News


class NewsView(ListView):
    """Новости на страницу"""
    model = News
    template_name = 'news/main.html'
    context_object_name = 'news'

class RegisterUser(CreateView):
    """Регистрация"""
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    # success_url = reverse_lazy('login')