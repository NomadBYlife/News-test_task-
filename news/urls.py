
from django.urls import path

from .views import NewsView, RegisterUserView, AllAuthorsView, Login, logout_user

urlpatterns = [
    path('', NewsView.as_view(), name='home'),
    path('all_authors/', AllAuthorsView.as_view(), name='all_author'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]