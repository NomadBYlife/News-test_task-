from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import views
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm, LoginUserForm, RaitingForm, NewsForm, SearchForm
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


class NewsListView(views.View):
    """Новости на страницу"""

    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        form = SearchForm()
        context = {
            'news': news,
            'menu': menu,
            'form': form,
        }
        return render(request, 'news/main.html', context)

    def post(self, request, *args, **kwargs):
        form = SearchForm()
        if request.POST['new'] == '-raiting':
            news = sorted(News.objects.all(), key=lambda n: n.raiting_sum(), reverse=True)
        if request.POST['new'] == '+raiting':
            news = sorted(News.objects.all(), key=lambda n: n.raiting_sum())
        if request.POST['new'] == '-date':
            news = News.objects.all().order_by('-date_create')
        if request.POST['new'] == '+date':
            news = News.objects.all().order_by('date_create')
        context = {
            'news': news,
            'menu': menu,
            'form': form,
        }
        return render(request, 'news/main.html', context)


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
            'my_score': my_score,
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
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(status=400)


class DeleteScoreView(views.View):
    """Удаляем оценку к статье"""

    def get(self, request, slug):
        ip = get_client_ip(request)
        score = Raiting.objects.get(new__slug=slug, ip=ip)
        score.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class Favorites(ListView):
    """Список избранных"""
    model = News
    template_name = 'news/favorites.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(pseudonym=self.request.user)
        context['news'] = News.objects.filter(favorites=author)
        return context


class FavoritesAdd(views.View):
    """Добавление в избранные"""

    @staticmethod
    def get(request, *args, **kwargs):
        news = News.objects.get(slug=kwargs['slug'])
        author = Author.objects.get(pseudonym=request.user)
        author.favorites.add(news)
        news.favorite = True
        news.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class FacoritesDelete(views.View):
    """Удаление из избранных"""

    @staticmethod
    def get(request, *args, **kwargs):
        news = News.objects.get(slug=kwargs['slug'])
        author = Author.objects.get(pseudonym=request.user)
        author.favorites.remove(news)
        news.favorite = False
        news.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class NewsAddView(CreateView):
    """Создание новой новости"""
    model = News
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


def search(request):
    form = SearchForm()

    context = {
        'form': form,
    }
    return render(request, )
