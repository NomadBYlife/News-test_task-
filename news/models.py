import datetime

from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from slugify import slugify


class News(models.Model):
    """Articles"""
    vendor_code = models.IntegerField(blank=True, null=True, verbose_name='vendor code')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True)
    short_description = models.TextField(max_length=250, verbose_name='short description')
    description = models.TextField()
    favorite = models.BooleanField(default=False)
    views = models.ManyToManyField('Ip', related_name='post_view', blank=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='date create')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

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
    """Author"""
    pseudonym = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    favorites = models.ManyToManyField(News, blank=True, related_name='favorites')
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta():
        ordering = ('id',)
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.pseudonym.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.pseudonym))
        return super().save(*args, **kwargs)


class Ip(models.Model):
    """Ips"""
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class RatingScore(models.Model):
    """Rating Score"""
    value = models.SmallIntegerField(default=0, verbose_name='score')

    class Meta:
        verbose_name = "Rating score"
        verbose_name_plural = "Rating scores"
        ordering = ['-value']

    def __str__(self):
        return f"{self.value}"


class Rating(models.Model):
    """Rating"""
    ip = models.CharField(max_length=15, verbose_name='IP adress')
    score = models.ForeignKey(RatingScore, on_delete=models.CASCADE)
    new = models.ForeignKey(News, on_delete=models.CASCADE, related_name='rating_news', verbose_name='article')

    class Meta:
        verbose_name = 'Score from users'
        verbose_name_plural = 'Scores from users'

    def __str__(self):
        return f"{self.score} - {self.new}"
