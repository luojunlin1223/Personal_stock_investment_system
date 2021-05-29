from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name='昵称', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    gender=models.CharField(max_length=8, verbose_name='性别', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

    def email_verified(self):
        if self.is_authenticated:
            result = EmailAddress.objects.filter(email=self.email)
            if len(result):
                return result[0].verified
        else:
            return False