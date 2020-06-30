from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validated_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        from MallShop.MallShop.settings import REGEX_MOBILE
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",  # 字段的值不能为空
                                     "required": "请输入验证码",  # 请求必须传这个字段
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 },
                                 help_text="验证码")

    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[
                                         UniqueValidator(queryset=User.objects.all(),
                                                         message="用户已经存在")])  # 用户唯一性验证，存在的用户名不能再次注册

    password = serializers.CharField(write_only=True, label="密码", style={'input_type': 'password'})

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by(
            '-add_time')  # initial_data,post提交的值
        if verify_records:
            last_records = verify_records[0]  # 最新的一条验证码
            print(type(last_records))
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_records.add_time.replace(tzinfo=None):  # 切换为不带时区的时间
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]  # 验证码code，删掉
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
