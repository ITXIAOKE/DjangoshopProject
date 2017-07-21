from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from xk_cart.models import CartInfo
from xk_user.models import UserInfo
from xk_user.user_decorator import user_islogin


# 服务器传给浏览器的值是什么类型，就是什么类型
# 浏览器传给服务器的值全部是字符串，要使用对应类型的值，就需要自己手动去转换
# session中的值都保存在服务器中，保存什么类型的值，取的时候就是什么类型的值

# 在列表页和详细页都可以加入购物车
def add(request):
    try:
        # 获取存储在浏览器中用户的id
        uid = request.session.get('uid')
        # 获取用户要添加到购物车的商品id
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))
        # user_id和goods_id都可以在xk_cart_cartinfo这个表中查询到
        cart = CartInfo.objects.filter(user_id=uid, goods_id=gid)

        if len(cart) == 1:  # 如果用户uid已经购买了商品gid，则将数量+count
            # 防止用户购买的商品数量大于库存的数量，在购物车页面出现1+100=101
            if cart[0].goods.gkucun < cart[0].count + count:
                return JsonResponse({'isadd': 2})
            else:
                cart[0].count += count
            cart[0].save()
        else:  # 用户uid没有购买gid过商品则添加用户id，商品id和商品数量
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        # 添加成功返回1，表示成功，
        return JsonResponse({'isadd': 1})
    except:
        # 添加失败返回0，表示失败
        return JsonResponse({'isadd': 0})


# 统计商品的个数
def count(request):
    uid = int(request.session.get('uid'))
    # 显示几种商品
    num_count = CartInfo.objects.filter(user_id=uid).count()  # 10
    # 显示总共添加几件商品
    # num_count=CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')#字典
    return JsonResponse({'count': num_count})


# 购物车页面
@user_islogin
def index(request):
    uid = int(request.session.get('uid'))
    # 一个用户的购物车中包含要购物的商品信息和该用户的基本信息
    cart_list = CartInfo.objects.filter(user_id=uid)
    context = {'title': '购物车', 'cart_list': cart_list, 'cart_show': 0}
    return render(request, 'xk_cart/cart.html', context)


# 用户在页面一修改商品的数量，就在数据库中修改一下数量count
def edit(request):
    # 拿到购物车的id
    id = int(request.GET.get('id'))
    count1 = int(request.GET.get('count'))
    cart = CartInfo.objects.get(pk=id)
    cart.count = count1
    cart.save()
    return JsonResponse({'ok': 1})


# 用户在页面删除一条商品信息，就在数据库中删除该条记录
def delete(request):
    id = int(request.GET.get('id'))
    cart = CartInfo.objects.get(id=id)
    cart.delete()
    return JsonResponse({'ok': 1})


def order(request):
    # 获取数据库中存取的用户id，根据该用户id，就可以找到该用户的信息
    user = UserInfo.objects.get(pk=request.session.get('uid'))
    # 把用户选中的商品提交到订单中
    # 注意：getlist的意思在页面中，只有name的input属性并且name的属性值为cart_id的商品才提交给订单页面
    # 通过购物车的id可以获取到用户要购物的商品和用户的信息
    cart_ids = request.POST.getlist('cart_id')  # 选中商品在购物车中的id=[5，6，7，8]是一个列表
    cart_list = CartInfo.objects.filter(id__in=cart_ids)
    # ','.join(cart_ids)是把cart_ids这个列表按照，逗号拼接成字符串
    context = {'title': '提交订单', 'user': user, 'cart_list': cart_list,
               'cart_ids': ','.join(cart_ids)}
    return render(request, 'xk_cart/order.html', context)
