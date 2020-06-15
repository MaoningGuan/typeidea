""" class-based view """
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from config.models import SideBar
from .models import Post, Tag, Category


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 处理首页的HTTP请求
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5  # 每页显示的记录数量
    context_object_name = 'post_list'  # 设置queryset的变量名称，用于在模板中调用
    template_name = 'blog/list.html'  # 渲染使用的模板文件


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据分类过滤 """
        queryset = super().get_queryset()  # 此处返回IndexView的queryset属性
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)  # 关键字参数：一对一外键category_id


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据标签过滤"""
        queryset = super().get_queryset()  # 此处返回IndexView的queryset属性
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)  # 关键字参数：多对多外键要tag__id


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'  # 设置传递到模板文件的变量名称
    pk_url_kwarg = 'post_id'  # 在DetailView中，会根据这个参数来过滤数据，如：post = queryset.filter(pk=post_id)
