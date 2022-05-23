from rest_framework import serializers

from .models import News, Author


class AuthorSerializer(serializers.ModelSerializer):
    """Вывоод автора"""
    pseudonym = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Author
        fields = ('pseudonym',)


class NewsListSerializer(serializers.ModelSerializer):
    """Вывод всех новостей"""
    total_views = serializers.IntegerField()
    rating_sum = serializers.IntegerField()
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['vendor_code', 'title', 'author', 'short_description', 'description', 'favorite', 'total_views',
                  'rating_sum', 'date_create']


class NewsForUpdateSerializer(serializers.ModelSerializer):
    """Обновления новости"""

    class Meta:
        model = News
        fields = ['title', 'short_description', 'description']


class NewsDetailSerializer(serializers.ModelSerializer):
    """Детализация новости"""
    rating_sum = serializers.IntegerField()
    author = AuthorSerializer(read_only=True)
    total_views = serializers.IntegerField()

    class Meta:
        model = News
        exclude = ['views']


class NewsCreateSerializer(serializers.ModelSerializer):
    """Создание новости"""

    class Meta:
        model = News
        fields = ['title', 'short_description', 'description']
