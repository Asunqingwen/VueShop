from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.

class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        用户收藏功能
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        """
        动态配置serializer_class
        :return:
        """
        if self.action == "list":
            return UserFavDetailSerializer  # 返回具体的serializer类
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)  # 获取当前用户的收藏列表


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)  # JWT和session验证，session验证用于browser API

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)  # 获取当前用户的留言列表


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)  # 获取当前用户的留言列表
