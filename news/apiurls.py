from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .apiviews import NewsListApiView, NewsDetailApiView, MyNewsApiView, MyNewsUpdateApiView, MyNewsFavoriteApiView, \
    MyNewsCreateApiView

urlpatterns = [
    path('news/', NewsListApiView.as_view()),
    path('news/<int:pk>', NewsDetailApiView.as_view()),
    path('news/my_news/', MyNewsApiView.as_view()),
    path('news/my_news/favorites/', MyNewsFavoriteApiView.as_view()),
    path('news/my_news/create/', MyNewsCreateApiView.as_view()),
    path('news/my_news/<int:pk>', MyNewsUpdateApiView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
