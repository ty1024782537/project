from django import forms
from django.core import validators

from order.models import ReceivingAddress


class ReceivingAddressForms(forms.ModelForm):
    class Meta:
        model = ReceivingAddress
        exclude = ['create_time', 'update_time', 'is_delete', 'user']
        error_messages = {
            'username': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'detailed_description': {
                'required': "请填写详细地址！",
            },
            'hcity': {
                'required': "请填写完整地址！",
            },
            'hproper': {
                'required': "请填写完整地址！",
            },
            'harea': {
                'required': "请填写完整地址！",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 验证手机号码格式错误
        self.fields['phone'].validators.append(validators.RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误'))

    def clean(self):
        # 验证如果数据库里地址已经超过6六条报错
        cleaned_data = super().clean()
        count = ReceivingAddress.objects.filter(is_delete=0, user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"hcity": "收货地址最多只能保存6条"})
        return cleaned_data
