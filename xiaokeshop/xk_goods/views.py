from django.shortcuts import render
from django.core.paginator import Paginator
from xk_goods.models import TypeInfo, GoodsInfo


def index(request):
    # 获取商品6种分类
    type_list = TypeInfo.objects.all()
    # 定义一个列表传递给上下文
    list_arr = []
    # 遍历6中类型
    for t in type_list:
        # 获取某种类型对应的所有商品，并按照id进行降序排列，取前4个商品信息进行展示
        new_list = t.goodsinfo_set.order_by('-id')[0:4]
        # 获取某种类型对应的所有商品，并按照点击量进行降序排列，取前4个商品信息进行展示
        click_list = t.goodsinfo_set.order_by('-gclick')[0:4]
        # 把最新的商品和点击量最高的商品以及该类商品的类型，用一个字典的形式添加到列表中
        list_arr.append({'new_list': new_list, 'click_list': click_list, 't_type': t})

    context = {'list_arr': list_arr, 'title': '首页', 'cart_show': 1}
    return render(request, 'xk_goods/index.html', context)


# tid是商品分类的id，pindex是显示第几页
def goods_list(request, tid, pindex, orderby):
    # 该商品属于那个类型
    t1 = TypeInfo.objects.get(pk=int(tid))

    # 默认排序，根据id进行降序排序
    orderby_str = '-id'
    # 默认价格是按照降序排列
    desc = 1
    # 点击了价格
    if int(orderby) == 2:
        # 通过get方式拿到页面中desc的值
        desc = request.GET.get('desc')
        if desc == '1':
            orderby_str = '-gprice'
        else:  # 是-1的情况
            orderby_str = 'gprice'
    # 点击了人气
    elif int(orderby) == 3:
        orderby_str = '-gclick'

    # 该类型下所有商品信息按照id降序排序后，取前两个最新的商品
    new_list = t1.goodsinfo_set.order_by('-id')[0:2]
    glist = t1.goodsinfo_set.order_by(orderby_str)

    # 每页显示10条信息
    paginator = Paginator(glist, 10)
    # 对页面个数进行容错处理判断
    page_new = int(pindex)
    if page_new <= 1:
        page_new = 1
    if page_new >= paginator.num_pages:
        page_new = paginator.num_pages
    # 显示第几页的信息，下标从1开始
    page = paginator.page(page_new)

    context = {'cart_show': '1', 'title': '商品列表', 't1': t1,
               'new_list': new_list, 'page': page
        , 'desc': desc, 'orderby': orderby}
    return render(request, 'xk_goods/list.html', context)


def detail(request, id):
    try:
        # filter返回【object】,没有对象，则返回空列表【】
        # get直接返回对象，没有对象，则会报错，需要自己手动处理
        goods = GoodsInfo.objects.get(pk=int(id))
        # 每点击一次商品，则商品的点击量就自动的加1
        goods.gclick += 1
        # 更新数据库信息
        goods.save()
        # 先找到当前商品的分类对象，再找到所有此分类的商品，然后按照id降序排列后，取其中最新的两个，在页面展示时是推荐的商品
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'cart_show': '1', 'title': '商品详细信息', 'new_list': new_list, 'goods': goods}
        response = render(request, 'xk_goods/detail.html', context)
        # 最近浏览的商品，在用户中心展示前5个
        # 先获取用户是否浏览过商品,[5,1,2,3,4]，切割方法一定是split，不能写错了
        ids = request.COOKIES.get('new_goods_ids', '').split(',')
        # 去重
        if id in ids:
            ids.remove(id)
        ids.insert(0, id)
        # 多于5个商品直接移除最后一个，不展示
        if len(ids) > 5:
            ids.pop()
        # 把用户浏览的商品id保存在cookie中
        response.set_cookie('new_goods_ids', ','.join(ids), max_age=60 * 60 * 24 * 7)
        return response
    # 建议以后都用这种的异常捕获方式
    except Exception as e:
        print(e)
        # 没有此商品，则返回404页面
        return render(request, '404.html')
