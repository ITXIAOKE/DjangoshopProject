from django.db import models


# 用户的模型类，用于生成表
class UserInfo(models.Model):
    # 注册时的用户名
    uname = models.CharField(max_length=20)
    # sha1加密，密码
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    # 收货人姓名，没有的时候直接设置为空
    ushou = models.CharField(default='', max_length=20)
    uaddress = models.CharField(default='', max_length=100)
    # 邮编
    ucode = models.CharField(default='', max_length=6)
    uphone = models.CharField(default='', max_length=11)
