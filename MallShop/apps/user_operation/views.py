from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserFav
from .serializers import UserFavSerializer, UserFavDetailSerializer
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
    queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
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
