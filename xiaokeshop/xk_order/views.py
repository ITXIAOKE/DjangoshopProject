from django.shortcuts import render, redirect
from django.db import transaction
import datetime
from xk_cart.models import CartInfo
from xk_order.models import OrderMain, OrderDetail

'''
下订单操作步骤：
1，创建主表
2，接收购物车id
3，遍历购物车
4，判断库存数量
5，如果库存足够，则
   a,创建详单
   b,修改数量
   c,删除购物车中提交订单的商品
   
6，如果库存不足，则回滚
7，计算总价
'''


# 给提交的订单进行逻辑的判断，判断成功后，重定向到用户中心的订单页面，失败回滚到购物车页面

# 加了@transaction.atomic之后，不会自动提交，需要自己手动的提交
@transaction.atomic
def do_order(request):
    # 创建一个点，用于在提交和回滚数据的时候，根据这个点来做相应的提交或者回滚
    sid=transaction.savepoint()
    # 用于记录是否提交成功，默认为提交成功
    is_commit=True
    try:
        # 获取请求的购物车信息
        cart_ids=request.POST.get('c_ids').split(',')
        # 创建订单主表
        main=OrderMain()
        # 格式化时间
        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 从session中拿到用户的id
        user_id = request.session.get('uid')
        # 拼接成主订单的id，也就是主键
        main.order_id = '%s%d' % (time_str, user_id)
        # 在主订单中保存用户的id
        main.order_user_id = user_id
        main.save()
        # 逐个遍历购物车中的商品，进行数量与库存的判断，
        # 根据已选中商品在购物车中id，过滤出所有选中的商品对应的购物车
        cart_list = CartInfo.objects.filter(id__in=cart_ids)
        total = 0
        # 遍历获取每一个购物车的信息
        for cart in cart_list:
            if cart.count <= cart.goods.gkucun:
                # 如果库存足够则添加到详单
                detail = OrderDetail()
                # 详单对应外键的主单
                detail.order = main
                detail.goods = cart.goods
                detail.count = cart.count
                detail.price = cart.goods.gprice
                # 计算所有商品的总价
                total += cart.count * cart.goods.gprice
                detail.save()
                # 修改库存
                cart.goods.gkucun -= cart.count
                cart.goods.save()
                # 删除购物车
                cart.delete()
            else:
                # 如果库存不够则购买失败回滚
                transaction.savepoint_rollback(sid)
                is_commit = False
                break
        if is_commit:
            # 改变主单的总价
            main.order_total_price = total
            main.save()
            transaction.savepoint_commit(sid)
    except Exception as e:
        print(e)
        is_commit = False
        transaction.savepoint_rollback(sid)
        # 返回response对象
    if is_commit:
        return redirect('/user/user_center_order/')
    else:
        return redirect('/cart/')


