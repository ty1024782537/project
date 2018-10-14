from django.conf.urls import url
from . import views as shopping

urlpatterns = [
    url(r'^$', shopping.Shopping_cart.as_view(), name='shopping'),
    url(r'^out_cart/$', shopping.Shopping_cartout.as_view(), name='out_cart')
]
