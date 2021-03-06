#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    # 设置富文本编辑器
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False,
                                 help_text="富文本编辑器")
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False,
                                 help_text="MarkDown文本编辑器（正文必须为MarkDown格式）")
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'is_md',
                  'content', 'content_md', 'content_ck', 'status')

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_file_name = 'content_md'
        else:
            content_file_name = 'content_ck'
        content = self.cleaned_data.get(content_file_name)
        if not content:
            self.add_error(content_file_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js', )
