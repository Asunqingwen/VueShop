from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    """
    接收UserFav模型传过来的post_save信号
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    """
    接收UserFav模型传过来的post_delete信号
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
