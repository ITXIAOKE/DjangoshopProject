# 给用户模块定义一个装饰器方法，用来判断用户是否登录
from django.shortcuts import redirect


def user_islogin(func):
    def in_func(request, *args, **kwargs):
        # 判断用户是否登录
        if request.session.has_key('uid'):
            # 用户已经登录过，则执行func函数
            return func(request, *args, **kwargs)
        else:
            # 用户没有登录
            return redirect('/user/login/')

    return in_func
