# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-17 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20200617_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=500, verbose_name='内容'),
        ),
    ]
