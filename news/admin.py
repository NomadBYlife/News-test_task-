from django.contrib import admin

from .models import News, RaitingScore, Raiting, Author


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка новостей"""
    list_display = ('vendor_code', 'title', 'slug', 'author', 'favorite', 'total_views')
    list_display_links = ('vendor_code', 'title')
    # list_editable = ('favorite',)
    exclude = ('slug',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """"""
    list_display = ('id', 'pseudonym')


@admin.register(RaitingScore)
class RaitingScoreAdmin(admin.ModelAdmin):
    """Админка оценок"""
    list_display = ('id', 'value')


@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    """Админка рейтинга"""
    list_display = ('id', 'ip', 'score', 'new')
