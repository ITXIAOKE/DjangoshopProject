from django.db import models

from xk_goods.models import GoodsInfo
from xk_user.models import UserInfo


# 订单的模型类


# 主订单
class OrderMain(models.Model):
    # 主订单的id号,自己规定的主键，例如20170714121212+用户id
    order_id = models.CharField(max_length=20, primary_key=True)
    # 订单创建时的时间
    order_time = models.DateTimeField(auto_now_add=True)
    # 创建订单的用户
    order_user = models.ForeignKey(UserInfo)
    # 所有订单的价钱,最大总共8位数，小数点后要两位，例如：888888.88
    order_total_price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    state=models.IntegerField(default=0)


# 单个订单，订单详情
class OrderDetail(models.Model):
    # 主订单与单个订单的关系是一对多的关系
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    # 每件商品的总价
    price = models.DecimalField(max_digits=5, decimal_places=2)
