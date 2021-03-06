"""MallShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import xadmin

from django.views.static import serve
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from .settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewset, HotSearchsViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset, AlipayView
from django.views.generic import TemplateView

# 配置goods的url
router = DefaultRouter()

# 配置goods的url
router.register('goods', GoodsListViewSet, basename='goods')

# 配置category的url
router.register('categorys', CategoryViewSet, basename='categorys')

# 配置验证码的url
router.register('codes', SmsCodeViewset, basename='codes')
router.register('hotsearchs', HotSearchsViewset, basename='hotsearchs')

router.register('users', UserViewset, basename='users')

# 收藏
router.register('userfavs', UserFavViewset, basename='userfavs')
# 留言
router.register('messages', LeavingMessageViewset, basename='messages')
# 收货地址
router.register('address', AddressViewset, basename='address')

# 购物车
router.register('shopcarts', ShoppingCartViewset, basename='shopcarts')
# 订单相关
router.register('orders', OrderViewset, basename='orders')

# 轮播图url
router.register('banners', BannerViewset, basename='banners')

# 首页商品系列数据
router.register('indexgoods', IndexCategoryViewset, basename='indexgoods')

schema_view = get_schema_view(
    openapi.Info(
        title="Lemon API接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="这是一个美轮美奂的接口文档",
        terms_of_service="http://api.keyou.site",
        contact=openapi.Contact(email="keyou100@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
)

# def trigger_error(request):
#     division_by_zero = 1 / 0

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # drf自带token认证模式
    # path('api-token-auth/', views.obtain_auth_token),

    # simple-jwt认证模式
    # simple-jwt认证模式
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('media/<path:path>', serve, {"document_root": MEDIA_ROOT}),

    # 三种不同风格的接口文档，自选其一
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', include_docs_urls(title="生鲜商城")),

    # router注册页
    path('', include(router.urls)),

    path('alipay/return/', AlipayView.as_view(), name="alipay"),

    path('index/', TemplateView.as_view(template_name="index.html"), name='index'),

    # 第三方登录
    path('extra/', include('social_django.urls', namespace='social')),

    #sentry验证
    # path('sentry-debug/', trigger_error),
]
