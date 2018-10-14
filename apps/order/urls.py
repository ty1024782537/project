from django.conf.urls import url
from . import views as order

urlpatterns = [
    url(r'^$', order.AllOrder.as_view(), name='order'),
    url(r'^tureorder/$', order.Tureorder.as_view(), name='tureorder'),
    url(r'^endorder/$', order.Order.as_view(), name='endorder'),
    url(r'^address/$', order.Address.as_view(), name='address'),
    url(r'^gladdress/$', order.Gladdress.as_view(), name='gladdress'),
    url(r'^delete/$', order.is_delete, name='delete'),  # 删除收货地址
    url(r'^editaddress/$', order.EditAddress.as_view(), name='editaddress'),  # 编辑收货地址页面
]
