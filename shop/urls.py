from django.conf.urls import url, include
from . import views as shop

urlpatterns = [
    url(r'^$', shop.Shop.as_view(), name='shop'),
    url(r'^store/$', shop.Store.as_view(), name='store'),
]
