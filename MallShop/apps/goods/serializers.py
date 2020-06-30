from rest_framework import serializers
from .models import Goods, GoodsCategory


class CategorySerializer3(serializers.ModelSerializer):
    """
    第三层商品类别序列化
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    第二层商品类别序列化
    """
    sub_cat = CategorySerializer3(many=True)  # model中对应变量定义的related_name属性,一对多

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    第一层商品类别序列化
    """
    sub_cat = CategorySerializer2(many=True)  # model中对应变量定义的related_name属性,一对多

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    # 序列化嵌套
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"
