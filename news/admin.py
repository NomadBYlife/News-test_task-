from django.contrib import admin

from .models import News, RatingScore, Rating, Author, Ip


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка новостей"""
    list_display = ('vendor_code', 'title', 'slug', 'author', 'favorite', 'rating_sum', 'total_views')
    list_display_links = ('vendor_code', 'title')
    exclude = ('slug', 'vendor_code')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админка авторов"""
    list_display = ('id', 'pseudonym')


@admin.register(RatingScore)
class RatingScoreAdmin(admin.ModelAdmin):
    """Админка оценок"""
    list_display = ('id', 'value')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Админка рейтинга"""
    list_display = ('id', 'ip', 'score', 'new')

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ['ip']