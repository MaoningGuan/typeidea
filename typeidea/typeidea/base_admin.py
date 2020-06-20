#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin


class BaseOwnerAdmin(object):
    """
    1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
    2、用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        """
        1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
        """
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        2、用来针对queryset过滤，只显示当前用户的数据
        :param request:
        :return:
        """
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


