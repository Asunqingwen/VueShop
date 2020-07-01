from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from .filters import GoodsFilter


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'pageSize'
    page_query_param = 'pageNum'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all().order_by("id")  # 分页需要先排序，不然会有UnorderedObjectListWarning
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    # authentication_classes = (TokenAuthentication,)

    # 过滤和搜索
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        商品分类详情页
    """
    queryset = GoodsCategory.objects.filter(category_type=1)  # 提取第一级目录
    serializer_class = CategorySerializer
