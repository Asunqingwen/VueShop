import json
import requests
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        clnt = YunpianClient(self.api_key)
        parmas = {
            YC.MOBILE: mobile,
            YC.TEXT: "您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }
        res = clnt.sms().single_send(parmas)
        return res


if __name__ == "__main__":
    yun_pian = YunPian("d6c4ddbf50ab36611d2f52041a0b949e")
    yun_pian.send_sms("2017", "15527473453")
