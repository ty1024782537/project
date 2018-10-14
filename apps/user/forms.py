import hashlib
# 验证码
# from captcha.fields import CaptchaField
from django import forms
from user import models
from user.models import User


# 登录表单
class UserForms(forms.Form):
    phone = forms.IntegerField(error_messages={
        'required': '手机是必填项'
    })
    password = forms.CharField(min_length=3, max_length=50
                               , error_messages={
            'required': '密码是必填项'
        })

    # 检测用户手机是否合格
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        rs = User.objects.filter(phone=phone).exists()
        if not rs:
            raise forms.ValidationError('账号不存在')
        if len(str(phone)) > 11:
            raise forms.ValidationError('手机号码超过11位')
        return phone


# 注册表单
class RegisterForm(forms.Form):
    phone = forms.IntegerField(
                               error_messages={
                                'required': '手机是必填项'
    })
    password = forms.CharField(min_length=3, max_length=50
                               , error_messages={
                                'required': '密码是必填项'
        })
    password2 = forms.CharField(min_length=3, max_length=50
                                , error_messages={
                                    'required': '确认密码是必填项'
        })
    code = forms.IntegerField(error_messages={
        'required': '验证码是必填项'})

    def clean_code(self):
        code = self.data.get('code')
        s_code = str(self.data.get('s_code'))
        if code != s_code:
            raise forms.ValidationError('验证码错误!')
        return code

    # 检测用户手机是否已经被注册
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        rs = User.objects.filter(phone=phone).exists()
        if rs:
            raise forms.ValidationError("该手机号码已经被注册!")
        if len(str(phone)) > 11:
            raise forms.ValidationError('手机号码超过11位')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError({"password2": "两次密码不一致!"})
        else:
            if all((password, password2)):
                h = hashlib.sha1(password.encode("utf-8"))
                pwd = h.hexdigest()
                cleaned_data['password'] = pwd
        return cleaned_data


# 修改个人信息
class IfonForm(forms.ModelForm):
    class Meta:
        model = models.User
        exclude = ['password', 'head', 'phone']
        error_messages = {
            'nickname': {
                'max_length': '昵称太长'
            },
            'school_name': {
                'max_length': '学校名太长'
            },
            'address': {
                'max_length': '地址写太长'
            },
            'hometown': {
                'max_length': '地址写太长'
            },
        }
