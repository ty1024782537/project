from django.conf.urls import url
from . import views as center

urlpatterns = [
    url(r'^$', center.PersonalCenter.as_view(), name='center'),
    url(r'^info/$', center.Info.as_view(), name='info'),
    url(r'^login/$', center.Login.as_view(), name='login'),
    url(r'^reg/$', center.Reg.as_view(), name='reg'),
    url(r'^forgetpw/$', center.Forgetpw.as_view(), name='forgetpw'),
    url(r'^logout/$', center.logout, name='logout'),
    url(r'^send_phone_code/$', center.send_phone_code, name='send_phone_code'),
]
