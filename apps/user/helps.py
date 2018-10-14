from aliyunsdkcore.client import AcsClient
from django.shortcuts import redirect, reverse
from project import settings
from user.models import User

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest

import uuid
from aliyunsdkcore.profile import region_provider


def clean_sql(phone, pwd):
    return User.objects.filter(phone=phone, password=pwd).first()


def clean_modification(id, nickname, gender, birthday, school_name, address, hometown, ):
    return User.objects.filter(pk=id).update(nickname=nickname, gender=gender, birthday=birthday,
                                             school_name=school_name, address=address, hometown=hometown)


# 登录验证装饰器
def login_required_view(func):
    def view(request, *args, **kwargs):
        if request.session.get('is_enter') is None:
            login_url = settings.LOGIN_URL
            return redirect(login_url)
        else:
            return func(request, *args, **kwargs)
    return view


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    # 注意：不要更改
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse
