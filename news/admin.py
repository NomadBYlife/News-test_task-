from django.contrib import admin

from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('vendor_code','title', 'slug', 'author','favorite')
    list_display_links = ('vendor_code', 'title')
    list_editable = ('favorite',)
    exclude = ('slug',)