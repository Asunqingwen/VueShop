from datetime import datetime

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.AliPay import AliPay
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from settings import private_key_path, ali_pub_key_path, notify_url, return_url, appid
from django.shortcuts import redirect


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能开发
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    lookup_field = "goods_id"  # 查询使用商品的ID，不使用购物记录的id

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


class AlipayView(APIView):
    def check_pay(self, params):
        """
        支付宝返回结果验签
        :param params:
        :return:
        """
        sign = params.pop('sign', None)  # 取出签名
        params.pop('sign_type')  # 取出签名类型
        params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
        message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
        try:
            with open(ali_pub_key_path) as public_key:  # 打开公钥文件
                status = verify_with_rsa(public_key.read().encode('utf-8').decode('utf-8'), message, sign)  # 验证签名并获取结果
                return status  # 返回验证结果
        except:
            return status

    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        params = request.GET.dict()  # 获取参数字典
        from pprint import pprint
        pprint(request.GET)
        response = redirect("index")
        if self.check_pay(params):
            order_sn = params.get('out_trade_no', None)
            trade_no = params.get('trade_no', None)
            trade_status = params.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
        response.set_cookie("nextPath", "pay", max_age=3)
        return response

    def post(self, request):
        """
        处理支付宝的notify_url返回
        :param request:
        :return:
        """
        params = request.POST.dict()  # 获取参数字典
        from pprint import pprint
        pprint(request.POST)
        if self.check_pay(params):
            order_sn = params.get('out_trade_no', None)
            trade_no = params.get('trade_no', None)
            trade_status = params.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            return Response("success")
