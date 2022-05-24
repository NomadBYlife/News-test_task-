from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import News, Author

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все авторы', 'url_name': 'all_author'}]


def get_client_ip(request):
    """Получаем айпи клиента"""
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


form_attributes = [('-rating', 'рейтингу (от большего к меньшему)'),
                   ('+rating', 'рейтингу (от меньшого к большому)'),
                   ('-date', 'дате (сначала новые)'),
                   ('+date', 'дате (сначала старые)'), ]

pagination_form_attributes = [('2', 2),
                              ('4', 4),
                              ('8', 8)]

def send(user_email):
    send_mail('Вы подписались на рассылку',
              'Спам будет лететь ;)',
              'vp3231963@gmail.com',
              [user_email],
              fail_silently=False,)
