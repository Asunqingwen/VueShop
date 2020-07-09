import time
from random import randint

from rest_framework import serializers
from goods.models import Goods
from goods.serializers import GoodsSerializer
from settings import private_key_path, notify_url, return_url, appid
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.AliPay import AliPay


class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车详情
    """
    goods = GoodsSerializer(many=False)  # 不是一对多，是一对一

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    # 获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label='数量', min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请选择购买数量",
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, label="商品", queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=appid,
            notify_url=notify_url,
            app_private_key_path=private_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=return_url
        )

        url = alipay.to_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        return url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    # 获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=appid,
            notify_url=notify_url,
            app_private_key_path=private_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=return_url
        )

        url = alipay.to_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        return url

    def generate_order_sn(self):
        """
        生成订单号
        :return:
        """
        # 当前时间+userid+随机数
        order_sn = "{time_str}{userid}{randstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                        userid=self.context["request"].user.id,
                                                        randstr=randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
