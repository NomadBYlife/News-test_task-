
from django.urls import path

from .views import NewsListView, RegisterUserView, AllAuthorsView, Login, logout_user, NewsDetailView

urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('news/<slug:slug>', NewsDetailView.as_view(), name='news_detail'),
    path('all_authors/', AllAuthorsView.as_view(), name='all_author'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]