from django.contrib import admin

# Register your models here.

from goods.models import GoodsSkuInfo, GoodsCategory, GoodsSpuInfo, GoodsUnit, GoodsImage, IndexImageBroadcast, \
    GoodsActivity, ActiveZone, GoodsActiveZone


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsSpuInfo)
class GoodsSpuInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsUnit)
class GoodsUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsImage)
class GoodsImageAdmin(admin.ModelAdmin):
    pass


class GoodsSkuInfoAdminInline(admin.TabularInline):
    model = GoodsImage
    extra = 2
    fields = ['image_address']


@admin.register(GoodsSkuInfo)
class GoodsSkuInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ['goods_name']
    search_fields = ['goods_name']  # 搜索框 搜索框'goods_name' 搜索里面的
    list_display_links = ['goods_name']  # 给goods_name设置一个A标签
    # 自定义项显示项
    list_display = ['id', 'goods_name', 'category', 'goods_price', 'goods_inventory', 'unit', 'goods_sales']
    inlines = [
        GoodsSkuInfoAdminInline
    ]
    fieldset = (
        ('基本信息', {'fields': ('goods_name', 'goods_price', 'unit', 'goods_inventory', 'goods_sales', 'is_shelf')}),
        ('详细信息', {'fields': ('intro', 'inventory')}),
    )


@admin.register(IndexImageBroadcast)
class IndexImageBroadcastAdmin(admin.ModelAdmin):
    pass
    # list_display = ['activity_name', 'image_address', 'url_address']


@admin.register(GoodsActivity)
class UserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ActiveZone)
class UserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsActiveZone)
class UserModelAdmin(admin.ModelAdmin):
    pass
