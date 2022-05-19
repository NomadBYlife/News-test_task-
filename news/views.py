
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import views
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm, LoginUserForm
from .models import News, Author, Ip

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все авторы', 'url_name': 'all_author'}]


def get_client_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class NewsListView(ListView):
    """Новости на страницу"""
    model = News
    template_name = 'news/main.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной сайт'
        context['menu'] = menu
        return context


class NewsDetailView(views.View):

    def get(self, request, *args,**kwargs):
        news = News.objects.get(slug=kwargs['slug'])
        ip = get_client_ip(request)
        if Ip.objects.filter(ip=ip).exists():
            news.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            news.views.add(Ip.objects.get(ip=ip))
        context = {
            'news': news,
            'menu': menu,
            'title': news,
        }
        return render(request, 'news/detailnews.html', context)


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
