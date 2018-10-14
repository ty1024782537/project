from django.shortcuts import render


from goods.models import GoodsCategory, GoodsSkuInfo


def goods(request, order=0):
    # 获取传过来的id
    ID = request.GET.get('id')
    # 传过来的类型是字符串要装换类型
    order = int(order)
    # 查询所有的分类信息
    goodscategory = GoodsCategory.objects.all()
    order_rule = ['id', '-goods_sales', '-goods_price', 'goods_price', '-create_time']
    order_rule_l = order_rule[order]
    if ID:
        ID = int(ID)
        goodscategor = GoodsCategory.objects.get(pk=ID)
        goodsskuinfo = goodscategor.goodsskuinfo_set.all()
        goodsskuinfo = goodsskuinfo.order_by(order_rule_l)
    else:
        ID = 1
        goodsskuinfo = goodscategory.first().goodsskuinfo_set.all()
        goodsskuinfo = goodsskuinfo.order_by(order_rule_l)
        return render(request, 'goods/category.html', locals())
    return render(request, 'goods/category.html', locals())


def detail(request, id):
    # goodsskuinfo = GoodsImage.objects.filter(goods_sku_id=id)
    # tt = goodsskuinfo.first().goods_sku
    # 查询商品信息
    goodsskuinfo = GoodsSkuInfo.objects.filter(pk=id).first()
    goodsimage = goodsskuinfo.goodsimage_set.all()
    return render(request, 'goods/detail.html', locals())
