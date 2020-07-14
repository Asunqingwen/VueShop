from django.db.models import Q
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner, HotSearchWords, GoodsCategoryBrand, IndexAd


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


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品轮播图
    """

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    # 序列化嵌套
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)  # 一对多

    class Meta:
        model = Goods
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False,
                                         context={'request': self.context['request']}).data  # 不加context参数，图像路径不会加上域名
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id), context={'request': self.context['request']})
        goods_serializer = GoodsSerializer(all_goods, many=True)
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
