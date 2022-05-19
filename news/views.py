from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import views
from django.views.generic import ListView, CreateView, DetailView

from .forms import RegisterUserForm, LoginUserForm, RaitingForm
from .models import News, Author, Ip, Raiting

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все авторы', 'url_name': 'all_author'}]


def get_client_ip(request):
    """Получаем айпи клиента"""
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
    """Детальное описание новости"""

    def get(self, request, *args, **kwargs):
        news = News.objects.get(slug=kwargs['slug'])
        ip = get_client_ip(request)
        if Ip.objects.filter(ip=ip).exists():
            news.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            news.views.add(Ip.objects.get(ip=ip))
        my_score = Raiting.objects.filter(new__slug=kwargs['slug'], ip=ip)
        if my_score.exists():
            has_score = 1
            my_score = my_score.first()
        else:
            has_score = 0
        context = {
            'news': news,
            'menu': menu,
            'title': news,
            'score_form': RaitingForm(),
            'has_score': has_score,
            'my_score' : my_score,
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
    """Логин"""
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все авторы'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Логаут"""
    logout(request)
    return redirect('home')


class AddScoreView(views.View):
    """Добавляем оценку к статье"""

    def post(self, request):
        form = RaitingForm(request.POST)
        if form.is_valid():
            Raiting.objects.update_or_create(
                ip=get_client_ip(request),
                new_id=int(request.POST.get('news')),
                defaults={'score_id': int(request.POST.get('score'))}
            )
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse(status=400)


class DeleteScoreView(views.View):
    """Удаляем оценку к статье"""

    def get(self, request, slug):
        ip = get_client_ip(request)
        score = Raiting.objects.get(new__slug=slug, ip=ip)
        score.delete()
        return redirect(request.META.get('HTTP_REFERER'))
