
from django.urls import path

from .views import NewsView, RegisterUser

urlpatterns = [
    path('', NewsView.as_view(), name='newsview'),
    path('register/', RegisterUser.as_view(), name='register')
]