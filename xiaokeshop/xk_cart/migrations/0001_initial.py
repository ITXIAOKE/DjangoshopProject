# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xk_user', '0001_initial'),
        ('xk_goods', '0002_auto_20170712_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='xk_goods.GoodsInfo')),
                ('user', models.ForeignKey(to='xk_user.UserInfo')),
            ],
        ),
    ]
