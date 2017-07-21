from  django.conf.urls import url
from xk_goods import views
from xk_goods.search_view import MySearchView

urlpatterns = [
    url(r'^$', views.index),
    # 商品列表页视图函数
    # 第一个是商品分类id，
    # 第二个是第几页的商品信息，默认都是显示第一页的商品信息
    # 第三个是点击默认还是人气还是价格
    # 问题：http://127.0.0.1:8000/list2_-4_1/中第二个，为负数何解？用-？
    url(r'^list(\d+)_(-?\d+)_(\d+)/$', views.goods_list),
    # 商品详情页视图函数
    url(r'^(\d+)/$', views.detail),
    url('^search/$',MySearchView.as_view()),

]
