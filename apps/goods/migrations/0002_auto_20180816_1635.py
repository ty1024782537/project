# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsskuinfo',
            name='goods_name',
            field=models.CharField(max_length=50, verbose_name='商品sku名'),
        ),
    ]
