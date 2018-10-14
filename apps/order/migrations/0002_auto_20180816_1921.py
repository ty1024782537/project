# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivingaddress',
            name='detailed_description',
            field=models.CharField(max_length=100, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='receivingaddress',
            name='is_address',
            field=models.BooleanField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='是否默认地址'),
        ),
    ]