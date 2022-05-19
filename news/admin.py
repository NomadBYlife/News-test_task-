from django.contrib import admin

from .models import News, Ip


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка новостей"""
    list_display = ('vendor_code', 'title', 'slug', 'author', 'favorite', 'total_views')
    list_display_links = ('vendor_code', 'title')
    list_editable = ('favorite',)
    exclude = ('slug',)

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')