from django.db import models
from tinymce.models import HTMLField


# 创建商品类型模型
class TypeInfo(models.Model):
    # 类型标题
    ttitle = models.CharField(verbose_name='标题',max_length=10)
    # 软删除标记
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


# 创建商品信息模型
class GoodsInfo(models.Model):
    # 商品大标题
    gtitle = models.CharField(verbose_name='大标题',max_length=20)
    gpic = models.ImageField(upload_to='goods/')
    gprice = models.DecimalField(verbose_name='价钱',max_digits=5, decimal_places=2)
    # 点击量
    gclick = models.IntegerField()
    # 单位 ：500g还是1瓶，还是一个
    gunit = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)
    # 商品小标题
    gsubtitle = models.CharField(max_length=200)
    # 商品库存
    gkucun = models.IntegerField(default=100)
    # 商品信息
    gcontent = HTMLField()
    # 关联关系，一对多
    gtype = models.ForeignKey('TypeInfo')
