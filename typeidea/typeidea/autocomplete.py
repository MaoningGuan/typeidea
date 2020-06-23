#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        # qs = Category.objects.filter(owner=self.request.user)
        qs = Category.objects.filter(status=Category.STATUS_NORMAL)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)  # 根据输入自动返回
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        # qs = Tag.objects.filter(owner=self.request.user)
        qs = Tag.objects.filter(status=Tag.STATUS_NORMAL)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)  # 根据输入自动返回
        return qs
