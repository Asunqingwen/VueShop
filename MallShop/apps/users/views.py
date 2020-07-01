from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets, status
from random import choice

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from .models import VerifyCode
from utils.yunpian import YunPian

# Create your views here.
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    用户自定义验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        from MallShop.MallShop.settings import APIKEY
        yun_pian = YunPian(APIKEY)

        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status.code() != 0:
            return Response({
                "mobile": sms_status.msg()
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """

    queryset = User.objects.all()

    authentication_classes = (JWTAuthentication, authentication.SessionAuthentication,)

    # serializer_class = UserRegSerializer
    def get_serializer_class(self):
        """
        动态配置serializer_class
        :return:
        """
        if self.action == "retrieve":
            return UserDetailSerializer  # 返回具体的serializer类
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        """
        动态配置permissions_classes
        :return:
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]  # 返回permissions的一个实例
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        refresh = RefreshToken.for_user(user)  # 手动添加jwt

        data = serializer.data
        # 生成jwt
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # 返回用户信息
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
