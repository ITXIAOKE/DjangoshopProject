from django.contrib import admin
from xk_goods.models import TypeInfo, GoodsInfo


# 注册商品类型和商品信息模型类
@admin.register(TypeInfo)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


# admin.site.register(TypeInfo, TypeAdmin)

@admin.register(GoodsInfo)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gprice']
    list_per_page = 10  # 每页显示15条信息

# admin.site.register(GoodsInfo, GoodsAdmin)
