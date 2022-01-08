from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True,verbose_name='аватарка')

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() +
                                            timedelta(hours=24)))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


