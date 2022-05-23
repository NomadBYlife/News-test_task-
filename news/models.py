from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from slugify import slugify


class News(models.Model):
    """Новости"""
    vendor_code = models.IntegerField(blank=True, null=True, verbose_name='артикул')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='слаг')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True, verbose_name='автор блога')
    short_description = models.TextField(max_length=250, verbose_name='краткое содержание')
    description = models.TextField(verbose_name='содержание')
    favorite = models.BooleanField(default=False, verbose_name='в избранном')
    views = models.ManyToManyField('Ip', related_name='post_view', blank=True, verbose_name='просмотры')
    date_create = models.DateTimeField(auto_now=True, verbose_name='дата публикации')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.vendor_code = self.id
        if not self.slug:
            self.slug = slugify(str(self.title))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def total_views(self):
        return self.views.count()

    def rating_sum(self):
        num = 0
        for i in self.rating_news.filter(new_id=self.pk):
            num += int(str(i.score))
        return num


class Author(models.Model):
    """Автор блога"""
    pseudonym = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='псевдоним')
    favorites = models.ManyToManyField(News, blank=True, related_name='favorites', verbose_name='избранные')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='слаг')

    class Meta():
        ordering = ('id',)
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self):
        return self.pseudonym.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.pseudonym))
        return super().save(*args, **kwargs)


class Ip(models.Model):
    """Айпи пользователей"""
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class RatingScore(models.Model):
    """Значения рейтинга"""
    value = models.SmallIntegerField(default=0, verbose_name='значение')

    class Meta:
        verbose_name = "возможная оценка"
        verbose_name_plural = "возможные оценки"
        ordering = ['-value']

    def __str__(self):
        return f"{self.value}"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    score = models.ForeignKey(RatingScore, on_delete=models.CASCADE, verbose_name='оценка')
    new = models.ForeignKey(News, on_delete=models.CASCADE, related_name='rating_news', verbose_name='статья')

    class Meta:
        verbose_name = 'поставленная оценка'
        verbose_name_plural = 'поставленные оценки'

    def __str__(self):
        return f"{self.score} - {self.new}"
