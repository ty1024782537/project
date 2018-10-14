# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hauling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('hauling_name', models.CharField(max_length=15, verbose_name='配送方式名字')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='金额')),
            ],
            options={
                'verbose_name': '配送方式管理',
                'verbose_name_plural': '配送方式管理',
                'db_table': 'hauling',
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('pay_name', models.CharField(max_length=15, verbose_name='支付名字')),
                ('pay_image', models.ImageField(upload_to='order/%Y%m/%d', verbose_name='支付方式图片')),
            ],
            options={
                'verbose_name': '支付方式管理',
                'verbose_name_plural': '支付方式管理',
                'db_table': 'pay',
            },
        ),
        migrations.CreateModel(
            name='ReceivingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号码')),
                ('hcity', models.CharField(default='北京', max_length=30, verbose_name='省')),
                ('hproper', models.CharField(default='北京', max_length=30, verbose_name='市')),
                ('harea', models.CharField(max_length=30, verbose_name='区')),
                ('detailed_description', models.CharField(max_length=100, verbose_name='详细描述')),
                ('is_address', models.BooleanField(choices=[(1, '否'), (0, '是')], default=1, verbose_name='是否默认地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '收货地址管理',
                'verbose_name_plural': '收货地址管理',
                'db_table': 'receivingaddress',
            },
        ),
    ]