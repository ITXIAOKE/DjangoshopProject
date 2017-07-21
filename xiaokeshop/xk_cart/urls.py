from django.conf.urls import url
from xk_cart import views

urlpatterns = [
    url(r'^$', views.index),
    url('^add/$', views.add),
    url('^count/$', views.count),
    url('^edit/$', views.edit),
    url('^delete/$', views.delete),
    url('^order/$', views.order),
]
