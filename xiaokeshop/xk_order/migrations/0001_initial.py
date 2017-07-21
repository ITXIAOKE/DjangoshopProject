# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xk_goods', '0002_auto_20170712_1252'),
        ('xk_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('goods', models.ForeignKey(to='xk_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('order_id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('order_total_price', models.DecimalField(max_digits=8, decimal_places=2, default=0)),
                ('state', models.IntegerField(default=0)),
                ('order_user', models.ForeignKey(to='xk_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='xk_order.OrderMain'),
        ),
    ]
