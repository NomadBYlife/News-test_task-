from django.contrib import admin

from .models import News, RatingScore, Rating, Author, Ip


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Articles"""
    list_display = ('vendor_code', 'title', 'slug', 'author', 'favorite', 'rating_sum', 'total_views')
    list_display_links = ('vendor_code', 'title')
    exclude = ('slug', 'vendor_code')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Authors"""
    list_display = ('id', 'pseudonym')


@admin.register(RatingScore)
class RatingScoreAdmin(admin.ModelAdmin):
    """Rating Score"""
    list_display = ('id', 'value')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating"""
    list_display = ('id', 'ip', 'score', 'new')

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    """IP"""
    list_display = ['ip']