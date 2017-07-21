from django.db import models

from xk_user.models import UserInfo


class CartInfo(models.Model):
    # 以下两种方式引入别的应用中模型类都是可以的
    goods = models.ForeignKey('xk_goods.GoodsInfo')
    user = models.ForeignKey(UserInfo)
    count=models.IntegerField()
