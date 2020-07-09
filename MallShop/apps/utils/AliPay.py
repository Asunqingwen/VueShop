import logging

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

from settings import appid, private_key_path, return_url, notify_url

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, notify_url, app_private_key_path, return_url, debug=False):
        self.return_url = return_url
        self.notify_url = notify_url
        self.alipay_client_config = AlipayClientConfig()  # 创建配置对象
        if debug is True:
            self.alipay_client_config.server_url = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.alipay_client_config.server_url = "https://openapi.alipay.com/gateway.do"
        self.alipay_client_config.app_id = appid  # APPID
        with open(app_private_key_path) as public_key:
            self.alipay_client_config.app_private_key = public_key.read()
        self.client = DefaultAlipayClient(alipay_client_config=self.alipay_client_config, logger=logger)  # 使用配置创建客户端

    def to_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        model = AlipayTradePagePayModel()  # 创建网站支付模型
        model.out_trade_no = out_trade_no  # 商户订单号码
        model.total_amount = total_amount  # 支付总额
        model.subject = subject  # 订单标题
        model.body = '一套完整详细的Python入门视频。'  # 订单描述
        model.product_code = 'FAST_INSTANT_TRADE_PAY'  # 与支付宝签约的产品码名称，目前只支持这一种。
        model.timeout_express = '30m'  # 订单过期关闭时长（分钟）
        pay_request = AlipayTradePagePayRequest(biz_model=model)  # 通过模型创建请求对象
        pay_request.notify_url = self.notify_url  # 设置回调通知地址（POST）
        pay_request.return_url = self.return_url  # 设置回调通知地址（GET）

        response = self.client.page_execute(pay_request, http_method='GET')  # 获取支付链接
        return response  # 重定向到支付宝支付页面


if __name__ == "__main__":
    alipay = AliPay(
        appid=appid,
        notify_url=notify_url,
        app_private_key_path=private_key_path,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        return_url=return_url
    )

    url = alipay.to_pay(
        subject="测试订单2",
        out_trade_no="20170202ssa",
        total_amount=100,
    )
    print(url)
