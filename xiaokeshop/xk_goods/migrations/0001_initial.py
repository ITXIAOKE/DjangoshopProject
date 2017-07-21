# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('gtitle', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to='goods/')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gclick', models.IntegerField()),
                ('gunit', models.CharField(max_length=10)),
                ('isDelete', models.BooleanField(default=False)),
                ('gsubtitle', models.CharField(max_length=200)),
                ('gkucun', models.IntegerField(default=100)),
                ('gcontent', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('ttitle', models.CharField(max_length=10)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='xk_goods.TypeInfo'),
        ),
    ]
