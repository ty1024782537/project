from django.shortcuts import render

from goods.models import IndexImageBroadcast, GoodsActivity, ActiveZone


def index(request):
    # 查询图片信息
    cast = IndexImageBroadcast.objects.all()
    # 首页活动信息
    goodsactivity = GoodsActivity.objects.all()
    # 首页专区活动信息
    activity = ActiveZone.objects.all()
    # for a in activity:
    #     c = a.goodsactivezone_set.all()
    return render(request, 'index/index.html', locals())
