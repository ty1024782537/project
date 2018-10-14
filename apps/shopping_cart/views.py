from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View
from goods.models import GoodsSkuInfo
from django_redis import get_redis_connection
from shopping_cart.helps import login_required_view


class Shopping_cart(View):
    @login_required_view
    def get(self, request):
        # 获取到保存到session里面的用户id
        user_id = request.session.get('user_id')
        # 获取key值
        hset_id = 'car_%s' % user_id
        # 使用默认配置连接到redis
        cnn = get_redis_connection('default')
        # 从Redis中查询出该用户保存的信息
        cart_info = cnn.hgetall(hset_id)
        # 总数
        count_all = 0
        # 总价格
        total_money = 0
        # 保存商品
        goods = []
        for goods_id, count in cart_info.items():
            goods_id = int(goods_id)
            count = int(count)
            count_all += count
            t = GoodsSkuInfo.objects.get(pk=goods_id)
            t.count = count
            goods_price = t.goods_price
            total_money += goods_price * count
            goods.append(t)
        return render(request, 'shopping_cart/shopcart.html', locals())

    def post(self, request):
        # 获取传过来的值
        sku_id = request.POST.get('car_id')
        count = request.POST.get('count')
        # 判断是否登录
        if request.session.get('is_enter') is None:
            return JsonResponse({'error': 1, 'emg': '请登录!', 'sku_id': sku_id})
        # 验证数据是否合法
        try:
            sku_id = int(sku_id)
            # print(sku_id)
            count = int(count)
        except:
            return JsonResponse({'error': 2, 'emg': '数据不合法!'})
        # 验证数据库是否存在该商品
        try:
            goods_sku = GoodsSkuInfo.objects.get(pk=sku_id)
        except:
            return JsonResponse({'error': 3, 'emg': '没有该商品!'})
        # 验证库存是否足够
        if count > goods_sku.goods_inventory:
            return JsonResponse({'error': 4, 'emg': '库存不足!'})
        # 保存到Redis
        # 使用默认配置连接到redis
        cnn = get_redis_connection('default')
        # 使用连接上的方法操作redis
        user_id = request.session.get('user_id')
        hset_id = 'car_%s' % user_id
        # 将hset_id添加到Redis里面
        cnn.hincrby(hset_id, sku_id, count)
        # 查询hset_id里面的所有数据  查询出来是一个集合需要遍历
        count_id = cnn.hvals(hset_id)
        car_count = 0
        for i in count_id:
            car_count += int(i)
        return JsonResponse({'error': 0, 'emg': '添加成功!', 'car_count': car_count})


class Shopping_cartout(View):
    def post(self, request):
        sku_id = request.POST.get('car_id')
        count = request.POST.get('count')
        # 判断是否登录
        if request.session.get('is_enter') is None:
            return JsonResponse({'error': 1, 'emg': '请登录!', 'sku_id': sku_id})
        # 验证数据是否合法
        try:
            sku_id = int(sku_id)
            # print(sku_id)
            count = int(count)
        except:
            return JsonResponse({'error': 2, 'emg': '数据不合法!'})
        # 验证数据库是否存在该商品
        try:
            goods_sku = GoodsSkuInfo.objects.get(pk=sku_id)
        except:
            return JsonResponse({'error': 3, 'emg': '没有该商品!'})
        # 保存到Redis
        # 使用默认配置连接到redis
        cnn = get_redis_connection('default')
        # 使用连接上的方法操作redis
        user_id = request.session.get('user_id')
        hset_id = 'car_%s' % user_id
        # 判断购物车中商品的数量是否 大于 1
        count = cnn.hget(hset_id, sku_id)
        if int(count) > 1:
            cnn.hincrby(hset_id, sku_id, -1)
        else:
            cnn.hdel(hset_id, sku_id)
        count_id = cnn.hvals(hset_id)
        car_count = 0
        for i in count_id:
            car_count += int(i)
        return JsonResponse({'error': 0, 'emg': '减少成功!', 'car_count': car_count})
