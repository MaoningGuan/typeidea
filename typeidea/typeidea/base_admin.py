#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin


class BaseOwnerAdmin(object):
    """
    1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
    2、用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def save_models(self):
        """
        1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
        """
        self.new_obj.owner = self.request.user
        return super().save_models()

    def get_list_queryset(self):
        """
        2、用来针对queryset过滤，只显示当前用户的数据
        :param request:
        :return:
        """
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)


