# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xk_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='gprice',
            field=models.DecimalField(max_digits=5, verbose_name='价钱', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gtitle',
            field=models.CharField(verbose_name='大标题', max_length=20),
        ),
        migrations.AlterField(
            model_name='typeinfo',
            name='ttitle',
            field=models.CharField(verbose_name='标题', max_length=10),
        ),
    ]
