# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-17 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20200617_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=2000, verbose_name='内容'),
        ),
    ]
