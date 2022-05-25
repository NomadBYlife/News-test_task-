from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import views
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm, LoginUserForm, RatingForm, NewsForm, SearchForm, PaginatorForm
from .models import News, Author, Ip, Rating
from .tasks import send_spam_email
from .utils import menu, get_client_ip, DataMixin


class NewsListView(views.View):
    """Новости на страницу"""

    def get(self, request, *args, **kwargs):
        news = News.objects.all().order_by('-date_create')
        paginator = Paginator(news, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = SearchForm()
        pag_form = PaginatorForm()
        context = {
            'title': 'Главная страница',
            'news': news,
            'menu': menu,
            'form': form,
            'page_obj': page_obj,
            'pag_form': pag_form,
        }
        return render(request, 'news/main.html', context)

    def post(self, request, *args, **kwargs):
        form = SearchForm()
        page_size = 2
        news = News.objects.all()
        if request.POST['new'] == '-rating':
            news = sorted(News.objects.all(), key=lambda n: n.rating_sum(), reverse=True)
        if request.POST['new'] == '+rating':
            news = sorted(News.objects.all(), key=lambda n: n.rating_sum())
        if request.POST['new'] == '-date':
            news = News.objects.all().order_by('-date_create')
        if request.POST['new'] == '+date':
            news = News.objects.all().order_by('date_create')
        pag_form = PaginatorForm()
        paginator = Paginator(news, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Главная страница',
            'page_obj': page_obj,
            'menu': menu,
            'form': form,
            'pag_form': pag_form,
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
        my_score = Rating.objects.filter(new__slug=kwargs['slug'], ip=ip)
        if my_score.exists():
            has_score = 1
            my_score = my_score.first()
        else:
            has_score = 0
        context = {
            'title': news.title,
            'news': news,
            'menu': menu,
            'score_form': RatingForm(),
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

    def form_valid(self, form):
        self.object = form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


class AllAuthorsView(DataMixin, ListView):
    """Список авторов"""
    model = Author
    template_name = 'news/authors_all.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Все авторы')
        return dict(list(context.items()) + list(cont.items()))


class Login(DataMixin, LoginView):
    """Логин"""
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Вход на сайт')
        return dict(list(context.items()) + list(cont.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Логаут"""
    logout(request)
    return redirect('home')


class AddScoreView(views.View):
    """Добавляем оценку к статье"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
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
        score = Rating.objects.get(new__slug=slug, ip=ip)
        score.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class Favorites(DataMixin, ListView):
    """Список избранных"""
    model = News
    template_name = 'news/favorites.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(pseudonym=self.request.user)
        context['news'] = News.objects.filter(favorites=author)
        cont = self.get_user_context(title='Избранные статьи')
        return dict(list(context.items()) + list(cont.items()))


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


class FavoritesDelete(views.View):
    """Удаление из избранных"""

    @staticmethod
    def get(request, *args, **kwargs):
        news = News.objects.get(slug=kwargs['slug'])
        author = Author.objects.get(pseudonym=request.user)
        author.favorites.remove(news)
        news.favorite = False
        news.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class NewsAddView(DataMixin, CreateView):
    """Создание новой новости"""
    model = News
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Добавление новой статьи')
        return dict(list(context.items()) + list(cont.items()))
