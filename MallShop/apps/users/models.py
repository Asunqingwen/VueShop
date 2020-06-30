from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户
    """
    # 新增字段
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    gender = models.CharField(max_length=6, choices=(('male', u"男"), ('female', u"女")), default='female',
                              verbose_name='性别')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='电话')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    # 类的实例对象str化，用于print，返回自定义数据会报错
    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码，后期变为redis存储
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')  # 这里默认的时间为程序运行时间，不是添加记录的时间

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    # 类的实例对象str化，用于print
    def __str__(self):
        return self.code
