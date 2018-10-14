from django.db import models
# 导入ckeditor上富文本编辑器自带字段
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from db.base_models import BaseModel

is_shelf = {
    (0, '上架'),
    (1, '下架'),
}


class GoodsCategory(BaseModel):
    category_name = models.CharField(verbose_name='分类名称', max_length=30)
    category_intro = models.CharField(verbose_name='分类简介', max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'category'
        verbose_name = '分类管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category_name


class GoodsSpuInfo(models.Model):
    goods_spu_name = models.CharField(verbose_name='商品名', max_length=20)
    goods_spu_intro = RichTextUploadingField(verbose_name='商品简介')

    class Meta:
        db_table = 'spuinfo'
        verbose_name = '商品SPU管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_spu_name


class GoodsUnit(BaseModel):
    unit_name = models.CharField(verbose_name='单位名', max_length=10)

    class Meta:
        db_table = 'goodsunit'
        verbose_name = '商品单位管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.unit_name


class GoodsSkuInfo(BaseModel):
    goods_name = models.CharField(verbose_name='商品sku名', max_length=50)

    def intro(self):
        return self.goods_intro

    intro.short_description = '商品简介'
    intro.allow_tags = True  # 允许展示html标签

    goods_intro = RichTextUploadingField(verbose_name='商品简介', )
    goods_price = models.FloatField(verbose_name='商品价格', )
    # on_delete = models.CASCADE级联删除
    unit = models.ForeignKey(to='GoodsUnit', on_delete=models.CASCADE, verbose_name="商品单位ID")
    goods_inventory = models.IntegerField(verbose_name='商品库存', default=0)
    goods_sales = models.IntegerField(verbose_name='商品销量', default=0)
    logo_address = models.ImageField(verbose_name='图片地址', upload_to="goods/%Y/%m/%d")
    is_shelf = models.BooleanField(verbose_name='是否上架', choices=is_shelf, default=0)

    def category(self):
        return self.goods_category.category_name

    category.short_description = '分类'

    goods_category = models.ForeignKey(to='GoodsCategory', on_delete=models.CASCADE, verbose_name='分类ID')
    goods_spu = models.ForeignKey(to='GoodsSpuInfo', on_delete=models.CASCADE, verbose_name='商品SPU_ID')

    class Meta:
        db_table = 'goodsskuinfo'
        verbose_name = '商品信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name


class GoodsImage(BaseModel):
    image_address = models.ImageField(verbose_name='图片地址', upload_to="image/%Y/%m/%d")
    goods_sku = models.ForeignKey(to='GoodsSkuInfo', on_delete=models.CASCADE, verbose_name='商品SkU_ID')

    class Meta:
        db_table = 'goodsimage'
        verbose_name = '图片信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_sku.goods_name


class IndexImageBroadcast(BaseModel):
    broadcast_name = models.CharField(verbose_name='轮播名称', max_length=100)
    goods_sku = models.ForeignKey(verbose_name='商品ID', to='GoodsSkuInfo')
    image_address = models.ImageField(verbose_name='图片地址', upload_to="user/%Y%m/%d")
    order = models.SmallIntegerField(verbose_name="排序", default=0)

    class Meta:
        db_table = 'broad'
        verbose_name = '首页轮播信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.broadcast_name


class GoodsActivity(models.Model):
    activity_name = models.CharField(verbose_name='活动名称', max_length=100)
    image_address = models.ImageField(verbose_name='图片地址', upload_to="user/%Y/%m/%d")
    url_address = models.CharField(verbose_name='路径', max_length=200)

    class Meta:
        db_table = 'broadcast'
        verbose_name = '首页活动信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


class ActiveZone(BaseModel):
    active_zone_name = models.CharField(verbose_name='专区活动名称', max_length=50)
    activity_description = models.CharField(verbose_name='活动描述', max_length=200, null=True, blank=True)
    order = models.SmallIntegerField(verbose_name="排序", default=0)
    is_shelf = models.BooleanField(verbose_name='是否上架', choices=is_shelf, default=0)

    class Meta:
        db_table = 'activezone'
        verbose_name = '首页专区活动信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.active_zone_name


class GoodsActiveZone(BaseModel):
    active_zone = models.ForeignKey(to='ActiveZone', verbose_name='专区活动ID')
    goods_sku = models.ForeignKey(to='GoodsSkuInfo', verbose_name='商品ID')

    class Meta:
        db_table = 'goodsactivezone'
        verbose_name = '首页专区活动商品管理表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.active_zone.active_zone_name
