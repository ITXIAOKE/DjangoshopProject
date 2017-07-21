from django.conf.urls import url
from xk_user import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_name/$', views.register_name),

    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),

    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),

    url(r'^logout/$', views.logout),
    url(r'^islogin/$', views.islogin),

]
