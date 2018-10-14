from django.db import models

# Create your models here.
from db.base_models import BaseModel
from user.models import User

is_address = {
    0: 'False',
    1: 'True'
}


class ReceivingAddress(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="用户ID")
    name = models.CharField(verbose_name='收货人姓名',
                            max_length=20, )
    phone = models.CharField(verbose_name='手机号码', max_length=11)
    hcity = models.CharField(verbose_name='省',
                             max_length=30,
                             default='北京', )
    hproper = models.CharField(verbose_name='市',
                               max_length=30,
                               default='北京', )
    harea = models.CharField(verbose_name='区',
                             max_length=30, )
    detailed_description = models.CharField(verbose_name='详细地址',
                                            max_length=100, )
    is_address = models.BooleanField(verbose_name='是否默认地址', default=False, blank=True)

    class Meta:
        db_table = 'receivingaddress'
        verbose_name = '收货地址管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class Pay(BaseModel):
    pay_name = models.CharField(verbose_name='支付名字',
                                max_length=15, )
    pay_image = models.ImageField(verbose_name='支付方式图片',
                                  upload_to="order/%Y%m/%d")

    class Meta:
        db_table = 'pay'
        verbose_name = '支付方式管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Hauling(BaseModel):
    hauling_name = models.CharField(verbose_name='配送方式名字',
                                    max_length=15, )
    money = models.DecimalField(verbose_name='金额',
                                max_digits=9,
                                decimal_places=2,
                                default=0
                                )

    class Meta:
        db_table = 'hauling'
        verbose_name = '配送方式管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hauling_name


class OrderInfo(BaseModel):
    order_status_choices = (
        (0, '待付款'),
        (1, '退发货'),
        (2, '待收货'),
        (3, '待评价'),
        (4, '已完成'),
        (5, '取消订单'),
    )
    """订单信息表"""
    order_sn = models.CharField(verbose_name="订单编号", max_length=150)
    order_money = models.DecimalField(verbose_name="订单金额", max_digits=9, decimal_places=2, default=0)
    user = models.ForeignKey(to=User, verbose_name="所属用户")
    receiver = models.CharField(verbose_name="收货人姓名", max_length=100)
    receiver_phone = models.CharField(verbose_name="收货人电话", max_length=11)
    address = models.CharField(verbose_name="收货人地址", max_length=200)
    order_status = models.SmallIntegerField(verbose_name="订单状态", choices=order_status_choices, default=0)
    transport = models.ForeignKey(to="Hauling", verbose_name="配送方式")
    transport_price = models.DecimalField(verbose_name="运费", max_digits=9, decimal_places=2, default=0)
    payment = models.ForeignKey(to="Pay", verbose_name="支付方式", null=True, blank=True)
    pay_money = models.DecimalField(verbose_name="实际支付金额", max_digits=9, decimal_places=2, default=0)
    description = models.CharField(verbose_name="备注说明", max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "订单基本信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(BaseModel):
    """订单商品表"""
    order = models.ForeignKey(to="OrderInfo", verbose_name="所属订单")
    goods_sku = models.ForeignKey(to='goods.GoodsSkuInfo', verbose_name="商品SKU")
    price = models.DecimalField(verbose_name="商品单价", max_digits=9, decimal_places=2, default=0)
    count = models.IntegerField(verbose_name="订单商品数量", default=0)

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.order.order_sn, self.goods_sku.goods_name)
