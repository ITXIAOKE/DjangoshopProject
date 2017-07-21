from django.conf.urls import url
from xk_order import views

urlpatterns = [
    url(r'^$', views.do_order)
]
