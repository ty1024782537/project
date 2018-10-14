import hashlib
import random

import re
import uuid
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, JsonResponse
from user import forms
from user.forms import UserForms, RegisterForm, IfonForm
from user.helps import clean_sql, clean_modification, login_required_view, send_sms
from user.models import User
from user.testing_view import BaseVerifyView


# 个人中心首页
class PersonalCenter(BaseVerifyView):
    def get(self, request):
        user = User.objects.filter(pk=5).first()
        return render(request, 'user/member.html', locals())

    def post(self, request):
        pass


# 用户信息
class Info(BaseVerifyView):
    # 获取用户信息
    def get(self, request):
        id = request.GET.get('id')
        user = User.objects.filter(pk=id).first()
        if user.birthday:
            user.birthday = user.birthday.strftime("%Y-%m-%d")
        context = {
            'user': user
        }
        return render(request, 'user/infor.html', context)

    # 修改用户信息
    def post(self, request):
        id = request.GET.get('id')
        info = request.POST
        postinfo = IfonForm(info)
        if postinfo.is_valid():
            user = postinfo.cleaned_data
            nickname = user['nickname']
            gender = user['gender']
            birthday = user['birthday']
            school_name = user['school_name']
            address = user['address']
            hometown = user['hometown']
            cm = clean_modification(id, nickname, gender, birthday, school_name, address, hometown)
            if cm:
                return redirect(reverse('user:center'))
        else:
            return redirect(reverse('user:info'))


# 短信验证码
def send_phone_code(request):
    # 获取提交过来的数据
    tel = request.GET.get('phone', '0')
    # print(tel)
    # 验证号码格式是否正确
    r = re.compile('^1[3-9]\d{9}$')
    # 在字符串中查找匹配正则表达式模式的位置，返回MatchObject的实例，如果没有找到匹配的位置，则返回None
    res = re.search(r, tel)
    # print(res)
    if res is None:
        return JsonResponse({"ok": 0, "msg": "手好号码格式错误!"})
    # 生成一个4位的随机数
    verification_code = random.randint(1000, 9999)
    print(verification_code)
    # 将随机数添加到session中
    request.session['code'] = verification_code
    # 设置过期时间60秒
    request.session.set_expiry(60)
    __business_id = uuid.uuid1()
    # print(__business_id)
    # params = "{\"code\":\"%s\"}" % verification_code
    # # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    # uu = send_sms(__business_id, tel, "滕洋", "SMS_142095023", params)
    # print(uu)
    # if uu:
    #     return JsonResponse({"ok": 1})
    # else:
    #     return HttpResponse('短信发送失败!')

    rc = {'ok': 1}
    if rc['ok'] == 1:
        return JsonResponse({"ok": 1})
    else:
        return HttpResponse('短信发送失败!')


# 登录页面
class Login(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        form = request.POST
        forms = UserForms(form)
        if forms.is_valid():
            data = forms.cleaned_data
            phone = data['phone']
            password = data['password']
            h = hashlib.sha1(password.encode("utf-8"))
            pwd = h.hexdigest()
            if all((phone, pwd)):
                user = clean_sql(phone, pwd)
                if user:
                    request.session['is_enter'] = True
                    request.session['user_id'] = user.id
                    request.session['phone'] = user.phone
                    request.session.set_expiry(0)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect(reverse('user:center'))
                else:
                    context = {
                        'errors': '密码错误'
                    }
                    return render(request, 'user/login.html', context)
        else:
            errors = forms.errors
            context = {
                'errors': errors
            }
            return render(request, 'user/login.html', context)


# 退出登录
def logout(request):
    if not request.session.get('is_enter', None):
        return redirect(reverse("index"))
    # request.session.clear()
    # request.session.flush()
    del request.session['is_enter']
    del request.session['user_id']
    del request.session['phone']
    return redirect(reverse('user:center'))


# 注册页面
class Reg(View):
    def get(self, request):
        reg_form = forms.RegisterForm()
        return render(request, 'user/reg.html', locals())

    def post(self, request):
        # 将session里面的code值取出来
        s_code = request.session.get('code')
        # 将code值添加到form表单进行验证
        data = request.POST.dict()
        data['s_code'] = s_code
        form_code = RegisterForm(data)
        if form_code.is_valid():
            user = form_code.cleaned_data
            phone = user['phone']
            password = user['password']
            if all((phone, password)):
                User.objects.create(phone=phone, password=password)
                return redirect('user:center')
        else:
            errors = form_code.errors
            context = {
                'errors': errors
            }
            return render(request, 'user/reg.html', locals())


# 忘记密码页面
class Forgetpw(View):
    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        pass
