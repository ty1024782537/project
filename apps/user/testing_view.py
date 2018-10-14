from django.utils.decorators import method_decorator
from django.views import View

from user.helps import login_required_view


class BaseVerifyView(View):
    """
        基础类视图，用于验证是否登录
    """
    @method_decorator(login_required_view)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseVerifyView, self).dispatch(request, *args, **kwargs)
