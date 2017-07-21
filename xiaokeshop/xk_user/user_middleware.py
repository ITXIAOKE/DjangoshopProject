# 定义一个用户模块中间件类，用于保存用户浏览的网页url，这样用户在登录之后，再次可以返回到之前浏览的网页


class UserUrlPathMiddleWare(object):
    # 在url请求之前，也就是用户输入完，url，还没有点击的时候
    # def process_request(self, request):
    #     # 如果当前请求的路径与用户登录、注册相关，则不需要记录
    #     if request.path not in ['/user/register/',
    #                             '/user/register_handle/',
    #                             '/user/register_name/',
    #                             '/user/login/',
    #                             '/user/login_handle/',
    #                             '/user/logout/', ]:
    #         request.session['session_url_path'] = request.get_full_path()


    # 在视图调用之前，调用这个方法
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 如果当前请求的路径与用户登录、注册相关，则不需要记录
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_name/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/islogin/', ]:
            request.session['session_url_path'] = request.get_full_path()


'''
http://www.baidu.cn/python?a=100
get_full_path():/python?a=100
path:/python
'''
