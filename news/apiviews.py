from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import News, Author
from .serializers import NewsListSerializer, NewsDetailSerializer, NewsForUpdateCreateSerializer



class MyCustomPagination(PageNumberPagination):
    """Custom pagination"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsListApiView(generics.ListAPIView):
    """List all articles"""
    serializer_class = NewsListSerializer
    queryset = News.objects.all().order_by('-date_create')
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ['date_create']
    ordering_fields = ['views']
    pagination_class = MyCustomPagination


class NewsDetailApiView(generics.RetrieveAPIView):
    """detail article"""
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()


class MyNewsApiView(generics.ListAPIView):
    """List of my articles"""
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = News.objects.filter(author__pseudonym=request._user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


class MyNewsUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    """Update one of my article"""
    queryset = News.objects.all()
    serializer_class = NewsForUpdateCreateSerializer
    permission_classes = [IsAuthenticated]


class MyNewsCreateApiView(generics.CreateAPIView):
    """Create new article"""
    serializer_class = NewsForUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = Author.objects.get(pseudonym=request._user)
        serializer.validated_data.update({'author': author})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyNewsFavoriteApiView(generics.ListAPIView):
    """List of favorite articles"""
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        author = Author.objects.get(pseudonym=self.request.user)
        self.queryset = News.objects.filter(favorites=author)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)