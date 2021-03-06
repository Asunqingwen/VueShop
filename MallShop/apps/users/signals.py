from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    """
    接收User模型传过来的post_save信号
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
