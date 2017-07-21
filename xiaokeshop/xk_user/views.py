from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from hashlib import sha1
from django.http import JsonResponse
import datetime
from xk_goods.models import GoodsInfo
from xk_order.models import OrderMain
from xk_user.models import UserInfo
from xk_user import user_decorator


def register(request):
    # 标题直接传给父模板
    context = {'title': '注册'}
    return render(request, 'xk_user/register.html', context)


# 注册校验与保存数据到mysql
def register_handle(request):
    # 服务器接受用户的post请求
    post = request.POST
    user_name = post.get('user_name')
    user_pwd = post.get('user_pwd').encode('utf-8')
    user_email = post.get('user_email')

    # 如果用户禁用js，那么需要在此，做一下校验
    # 也就是客户端的验证可能不准确，需要在做一个校验

    # 密码sha1加密
    s1 = sha1()
    s1.update(user_pwd)
    sha1_pwd = s1.hexdigest()

    # 把数据保存到mysql数据库中
    user = UserInfo()
    user.uname = user_name
    user.upwd = sha1_pwd
    user.uemail = user_email
    user.save()

    # 重定向到登录页面
    return redirect('/user/login/')


# 注册时，用户名的校验
def register_name(request):
    # 拿到用户注册时的用户名,使用ajax回调函数
    get_user_name = request.GET.get('get_user_name')
    # 从mysql中查询当前注册用户名的个数
    number = UserInfo.objects.filter(uname=get_user_name).count()
    # 返回json数据{'num':0或者1}
    context = {'num': number}
    return JsonResponse(context)


def login(request):
    # 从浏览器中读取存储的name信息，如果没有name，则默认给’‘，否则浏览器显示none
    get_cookie_login_user_name = request.COOKIES.get('set_cookie_login_user_name', '')
    context = {'title': '登录', 'show_login_user_name': get_cookie_login_user_name}
    return render(request, 'xk_user/login.html', context)


def login_handle(request):
    post = request.POST
    # 读取用户输入的用户名和密码
    login_name = post.get('login_user_name')
    login_pwd = post.get('login_user_pwd').encode('utf-8')
    # 用户选中记住密码为1，没有选中记住密码为0
    login_jz = post.get('user_jz', 0)

    # 密码sha1加密
    s2 = sha1()
    s2.update(login_pwd)
    sha1_login_pwd = s2.hexdigest()

    # 定义上下文
    context = {'title': '登录', 'show_login_user_name': login_name, 'show_login_user_pwd': login_pwd}

    # 向mysql数据库中查询数据，查到返回【UserInfo】,没有则返回[]
    result = UserInfo.objects.filter(uname=login_name)
    if len(result) == 0:  # 返回的列表中没有数据
        # 用户名不存在
        context['error_name'] = '亲！用户名输入错误'
        return render(request, 'xk_user/login.html', context)
    else:
        # 用户名可用，校验密码
        if result[0].upwd == sha1_login_pwd:
            # 登录成功，重定向到用户登录之前浏览的页面，/表示是首页
            response = redirect(request.session.get('session_url_path', '/'))
            # session中保存用户id和用户uname
            # uid在用户中心和头部使用
            request.session['uid'] = result[0].id
            # session_name在头部使用，用于显示用户，例如：欢迎晓可
            request.session['session_name'] = result[0].uname
            # 用户勾选记住用户名
            if login_jz == '1':
                response.set_cookie('set_cookie_login_user_name', login_name,
                                    expires=datetime.datetime.now() + datetime.timedelta(days=14))
            else:  # 用户没有勾选记住用户名
                response.set_cookie('set_cookie_login_user_name', '', max_age=-1)
            return response
        else:
            # 密码错误
            context['error_pwd'] = '亲！密码输入错误'
            return render(request, 'xk_user/login.html', context)


@user_decorator.user_islogin
def user_center_info(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    # 获取用户最近浏览的商品id
    ids = request.COOKIES.get('new_goods_ids', '').split(',')
    # 用一个列表装商品id
    glist = []
    for id in ids:
        # 用户没有浏览商品
        if id != '':
            glist.append(GoodsInfo.objects.get(id=id))

    context = {'user': user, 'title': '用户中心', 'glist': glist}
    return render(request, 'xk_user/user_center_info.html', context)


@user_decorator.user_islogin
def user_center_order(request):
    # 根据当前登录的用户，查询当前登录用户的订单并分页，OrderMain是主订单，例如【13,34,12,34,56】
    order_list = OrderMain.objects.filter(order_user_id=request.session.get('uid'))
    # 拿到分页对象，每页显示3个商品信息
    paginator = Paginator(order_list, 3)
    # 获得第几页的信息，默认返回第一页面中对象信息
    pindex = int(request.GET.get('pindex', '1'))
    # 返回对应页码中页面对象的信息，下标从1开始
    page = paginator.page(pindex)

    # 分页页码
    page_list = []
    if paginator.num_pages < 5:
        page_list = paginator.page_range
    elif pindex <= 2:
        page_list = range(1, 6)
    elif pindex >= paginator.num_pages - 1:
        page_list = range(paginator.num_pages - 4, paginator.num_pages + 1)
    else:
        page_list = range(pindex - 2, pindex + 3)

    context = {'title': '用户订单', 'order_page': page, 'page_list': page_list}
    return render(request, 'xk_user/user_center_order.html', context)


@user_decorator.user_islogin
def user_center_site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        shou_name = post.get('shou_name')
        uaddress = post.get('uaddress')
        ucode = post.get('ucode')
        uphone = post.get('uphone')
        # 修改用户的信息
        user.ushou = shou_name
        user.uaddress = uaddress
        user.ucode = ucode
        user.uphone = uphone
        user.save()

    context = {'user': user, 'title': '用户地址'}
    return render(request, 'xk_user/user_center_site.html', context)


# 退出用户
def logout(request):
    request.session.flush()
    return redirect('/user/login/')


# 判断用户是否登录过
def islogin(request):
    result = 0
    if request.session.has_key('uid'):
        result = 1
    return JsonResponse({'islogin': result})
