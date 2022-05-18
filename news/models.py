from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


class News(models.Model):
    """Новости"""
    vendor_code = models.IntegerField(verbose_name='артикул')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='слаг')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    short_description = models.TextField(max_length=250, verbose_name='краткое содержание')
    description = models.TextField(verbose_name='содержание')
    favorite = models.BooleanField(default=False, verbose_name='в избранном')
    # my_mark
    # raiting

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        return super().save(*args, **kwargs)

