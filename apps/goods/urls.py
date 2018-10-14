from django.conf.urls import url, include
# 设置Redis缓存
from django.views.decorators.cache import cache_page

from . import views as index

urlpatterns = [
    url(r'^(?P<order>\d).html/$', cache_page(60)(index.goods), name='index'),
    url(r'^detail/(?P<id>\d+)/$', index.detail, name='detail'),
]
