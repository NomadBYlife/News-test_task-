
from django.urls import path

from .views import NewsListView, RegisterUserView, AllAuthorsView, Login, logout_user, NewsDetailView, AddScoreView, \
    DeleteScoreView, FavoritesAdd, FacoritesDelete, Favorites, NewsAddView


urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('news/news_add', NewsAddView.as_view(), name='news_add'),
    path('news/<slug:slug>', NewsDetailView.as_view(), name='news_detail'),
    path('add-score/', AddScoreView.as_view(), name='add_score'),
    path('delete-score/<slug:slug>', DeleteScoreView.as_view(), name='delete_score'),
    path('all_authors/', AllAuthorsView.as_view(), name='all_author'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('favorites/', Favorites.as_view(), name='favorites'),
    path('favorites_add/<slug:slug>', FavoritesAdd.as_view(), name='favorites_add'),
    path('favorites_delete/<slug:slug>', FacoritesDelete.as_view(), name='favorites_delete'),

]
