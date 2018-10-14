from datetime import datetime
import random

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from goods.models import GoodsSkuInfo
from order.forms import ReceivingAddressForms
from order.models import Hauling, ReceivingAddress, OrderInfo, OrderGoods
from user.models import User
from user.testing_view import BaseVerifyView


# 全部订单
class AllOrder(View):
    def get(self, request):
        orderInfo = OrderInfo.objects.all()
        return render(request, 'order/allorder.html', locals())


# 提交订单页面
class Tureorder(BaseVerifyView):
    def get(self, request):
        # 获取到保存到session里面的用户id
        user_id = request.session.get('user_id')
        # 获取提交过来的skus  获取一个(request.GET.get('skus'))  获取提交过来的多个值(request.GET.getlist('skus'))
        sku_id = request.GET.getlist('skus')
        # print(sku_id)
        # 总价格
        total_money = 0
        order_goods = []
        hauling = Hauling.objects.all()
        for i in sku_id:
            # 获取key值
            hset_id = 'car_%s' % user_id
            # 使用默认配置连接到redis
            cnn = get_redis_connection('default')
            t = GoodsSkuInfo.objects.get(pk=i)
            # 从Redis中查询出该用户保存的信息
            count = cnn.hget(hset_id, i)
            count = int(count)
            t.count = count
            goods_price = t.goods_price
            total_money += goods_price * count
            order_goods.append(t)
        receivingAddress = ReceivingAddress.objects.filter(is_address=1, is_delete=0).first()
        # print(receivingAddress)
        return render(request, 'order/tureorder.html', locals())

    # 事务
    @transaction.atomic
    def post(self, request):
        """
            1. 收货地址address_id
            2. 商品sku_ids(多个 request.POST.getlist("sku_ids"))
            3. 配送方式transport
        """
        # 获取到保存到session里面的用户id
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except:
            return JsonResponse({'error': 1, 'erg': '登录错误!'})
        # 获取请求的数据
        address_id = request.POST.get('address_id')
        transport_id = request.POST.get('transport')
        sku_id = request.POST.getlist('sku_id')
        # 判断请求的数据
        if not all((address_id, transport_id, sku_id)):
            return JsonResponse({'error': 2, 'erg': '参数错误!'})
        # 收货地址
        try:
            address = ReceivingAddress.objects.filter(is_delete=0, user_id=user_id).get(pk=address_id)
        except:
            return JsonResponse({'error': 3, 'erg': '获取地址不纯在!'})
        # 配送方式
        try:
            transport = Hauling.objects.filter(is_delete=0).get(pk=transport_id)
        except:
            return JsonResponse({'error': 4, 'erg': '配送方式不纯在!'})

        """
        添加订单数据
        """
        # 设置一个保存点,(事务回滚,回滚到该位置)以后回滚到该保存点位置
        sid = transaction.savepoint()

        # 生成一个订单编号
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), random.randint(1000, 9999), user_id)
        # 生成一个地址
        order_address = '{}{}{}{}'.format(address.hcity, address.hproper, address.harea, address.detailed_description)
        print(order_address)
        print(order_sn)
        try:
            orderInfo = OrderInfo.objects.create(
                order_sn=order_sn,
                user=user,
                receiver=address.name,
                receiver_phone=address.phone,
                address=order_address,
                transport=transport,
                transport_price=transport.money,
            )
            print(orderInfo)
        except:
            return JsonResponse({'error': 5, 'erg': '订单添加失败!'})

        # 连接redis
        cnn = get_redis_connection("default")
        hset_id = 'car_%s' % user_id

        # 定义一个订单总价格
        order_money = 0
        # 获取商品信息
        for skuid in sku_id:
            try:
                goods_sku = GoodsSkuInfo.objects.select_for_update().get(pk=skuid)  # 加锁(解决高并发问题)
            except:
                # 手动回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"error": 6, "msg": "商品不存在!"})

            # 获取购物车中商品的数量
            count = cnn.hget(hset_id, skuid)
            print(count)
            count = int(count)

            # 判断库存是否足够
            if goods_sku.goods_inventory < count:
                # 手动回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"error": 7, "msg": "商品库存不足!"})

            # 保存订单商品表的数据
            try:
                order_goods = OrderGoods.objects.create(
                    order=orderInfo,
                    goods_sku=goods_sku,
                    price=goods_sku.goods_price,
                    count=count
                )
            except:
                # 手动回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"error": 8, "msg": "创建订单商品数据失败!"})

            # 订单商品表保存成功, 说明该商品的库存减少
            goods_sku.goods_inventory -= count
            # 销量增加
            goods_sku.goods_sales += count
            goods_sku.save()

            # 累计计算订单总价
            order_money += count * goods_sku.goods_price

        # 将订单商品总价保存在订单基本信息表中
        try:
            orderInfo.order_money = order_money
            orderInfo.save()
        except:
            # 手动回滚事务
            transaction.savepoint_rollback(sid)
            return JsonResponse({"error": 9, "msg": "更新订单价格失败!"})

        # 清空购物车
        cnn.hdel(hset_id, *sku_id)
        # 提交事务
        transaction.savepoint_commit(sid)

        return JsonResponse({"error": 0, "msg": "创建订单成功", "order_sn": order_sn})


# 确认订单页面
class Order(View):
    def get(self, request):
        # 获取用户ID
        user_id = request.session.get('user_id')
        # 获取提交过来的订单数据
        order_sn = request.GET.get('order_sn')
        # 查询订单基本数据
        orderinfo = OrderInfo.objects.filter(user_id=user_id).get(order_sn=order_sn)
        # 实际支付金额
        goods_price = orderinfo.order_money + orderinfo.transport_price

        ordergoods = orderinfo.ordergoods_set.all()
        return render(request, 'order/order.html', locals())


# 收货地址页面
class Address(BaseVerifyView):
    def get(self, request):
        return render(request, 'order/address.html')

    def post(self, request):
        # 验证数据的的合法性
        data = request.POST.dict()
        data['user_id'] = request.session.get("user_id")
        add_form = ReceivingAddressForms(data)
        if add_form.is_valid():
            # 判断是否将当期地址设置为默认收货地址
            if add_form.cleaned_data.get('is_address'):
                # 将该用户的其他收货地址设置为false
                ReceivingAddress.objects.filter(user_id=request.session.get("user_id")).update(is_address=0)
            # 保存的时候必须有用户的id
            add_form.instance.user_id = request.session.get("user_id")
            add_form.save()
            return JsonResponse({"error": 0})
        else:
            return JsonResponse({"error": 1, "errors": add_form.errors})


# 管理收货地址页面
class Gladdress(BaseVerifyView):
    def get(self, request):
        address = ReceivingAddress.objects.filter(is_delete=0).order_by('-is_address')
        return render(request, 'order/gladdress.html', locals())

    def post(self, request):
        # 获取到post提交过来的id
        address_id = request.POST.get('address_id')
        ReceivingAddress.objects.filter(is_address=1).update(is_address=0)
        ress = ReceivingAddress.objects.filter(pk=address_id).update(is_address=1)
        if ress:
            return JsonResponse({'ok': 1})
        else:
            return JsonResponse({'ok': 0})


# 删除收货地址
def is_delete(request):
    id = request.POST.get('id')
    ress = ReceivingAddress.objects.filter(pk=id).update(is_delete=1)
    if ress:
        return JsonResponse({'ok': 1})


# 编辑收货地址
class EditAddress(BaseVerifyView):
    def get(self, request):
        address_id = request.GET.get('id')
        ress = ReceivingAddress.objects.filter(pk=address_id).first()
        return render(request, 'order/editaddress.html', locals())

    def post(self, request):
        pass
