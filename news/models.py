from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from slugify import slugify


class News(models.Model):
    """Новости"""
    vendor_code = models.IntegerField(verbose_name='артикул')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='слаг')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='автор блога')
    short_description = models.TextField(max_length=250, verbose_name='краткое содержание')
    description = models.TextField(verbose_name='содержание')
    favorite = models.BooleanField(default=False, verbose_name='в избранном')
    views = models.ManyToManyField('Ip', related_name='post_view', blank=True, verbose_name='просмотры')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def total_views(self):
        return self.views.count()

    def raiting_sum(self):
        num = 0
        for i in self.raiting_news.filter(new_id=self.pk):
            num += int(str(i.score))
        return num


class Author(models.Model):
    """Автор блога"""
    pseudonym = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='псевдоним')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='слаг')

    class Meta():
        ordering = ('id',)
        verbose_name = 'блогер'
        verbose_name_plural = 'блогеры'

    def __str__(self):
        return self.pseudonym.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.pseudonym))
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(pseudonym=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.author.save()


class Ip(models.Model):
    """Айпишники"""
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class RaitingScore(models.Model):
    """Значения рейтинга"""
    value = models.SmallIntegerField(default=0, verbose_name='значение')

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
        ordering = ['-value']

    def __str__(self):
        return f"{self.value}"


class Raiting(models.Model):
    """Рейтинг"""
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    score = models.ForeignKey(RaitingScore, on_delete=models.CASCADE, verbose_name='оценка')
    new = models.ForeignKey(News, on_delete=models.CASCADE, related_name='raiting_news', verbose_name='статья')

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'

    def __str__(self):
        return f"{self.score} - {self.new}"
