from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import News, Author
from .serializers import NewsListSerializer, NewsDetailSerializer, NewsForUpdateSerializer, NewsCreateSerializer



class MyCustomPagination(PageNumberPagination):
    """Кастомная пагинация"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsListApiView(generics.ListAPIView):
    """Список всех новостей"""
    serializer_class = NewsListSerializer
    queryset = News.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ['date_create']
    ordering_fields = ['date_create', 'views']
    pagination_class = MyCustomPagination


class NewsDetailApiView(generics.RetrieveAPIView):
    """Детализация определенной новости"""
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()


class MyNewsApiView(generics.ListAPIView):
    """Список новостей моих как автора"""
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = News.objects.filter(author__pseudonym=request._user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


class MyNewsUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение одной из моих новостей"""
    queryset = News.objects.all()
    serializer_class = NewsForUpdateSerializer
    permission_classes = [IsAuthenticated]


class MyNewsCreateApiView(generics.CreateAPIView):
    """Создание новой статьи"""
    serializer_class = NewsCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = Author.objects.get(pseudonym=request._user)
        serializer.validated_data.update({'author': author})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyNewsFavoriteApiView(generics.ListAPIView):
    """Список избранных новостей"""
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        author = Author.objects.get(pseudonym=self.request.user)
        self.queryset = News.objects.filter(favorites=author)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)