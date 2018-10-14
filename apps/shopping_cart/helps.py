# 登录验证装饰器
from django.shortcuts import redirect

from project import settings


def login_required_view(func):
    def view(self, request, *args, **kwargs):
        if request.session.get('is_enter') is None:
            login_url = settings.SHOPPING_URL
            return redirect(login_url)
        else:
            return func(self, request, *args, **kwargs)
    return view
