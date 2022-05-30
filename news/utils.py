from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import News, Author

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все авторы', 'url_name': 'all_author'}]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


def get_client_ip(request):
    """Getting client IP"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(post_save, sender=News)
def create_news_vendor_code(sender, instance, created, **kwargs):
    if created:
        instance.vendor_code = instance.id
        instance.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(pseudonym=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.author.save()


form_attributes = [('-rating', 'rating (from largest to smallest)'),
                   ('+rating', 'rating (from smallest to largest)'),
                   ('-date', 'date (first new)'),
                   ('+date', 'дате (first old)'), ]

pagination_form_attributes = [('2', 2),
                              ('4', 4),
                              ('8', 8)]


def send(user_email):
    send_mail('You are subscribed to the newsletter',
              'Spam will fly ;)',
              'vp3231963@gmail.com',
              [user_email],
              fail_silently=False, )
